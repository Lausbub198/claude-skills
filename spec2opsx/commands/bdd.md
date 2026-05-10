# OPSX: BDD Feature File Generation

> **Portability note:** This file lives in two places:
> - `~/.claude/commands/opsx/bdd.md` — global fallback, used in any project
> - `.claude/commands/opsx/bdd.md` — project-local copy (takes precedence), should be committed to the repo
>
> When setting up a new project, copy this file into `.claude/commands/opsx/` alongside the other opsx commands. Update the copy whenever the OpenSpec framework changes its directory conventions.
>
> Written against **openspec 1.3.0**. If `openspec --version` returns a higher major version, check the changelog before using.

Generate Gherkin `.feature` files and step stubs from an OpenSpec change's spec files.

**Output (paths depend on detected project layout — see Step 2):**
- One `.feature` file per spec, scenarios tagged `@platform`
- One step stub file per platform, all steps with a "not implemented" throw/raise

**Input**: Optionally specify a change name and `--force` flag (e.g., `/opsx:bdd foundation`, `/opsx:bdd foundation --force`). If omitted, infer from context.

---

## Steps

### 1. Select the change and verify framework version

```bash
openspec --version 2>/dev/null || echo "NOT_FOUND"
```

- If `NOT_FOUND`: abort — "openspec CLI not found. Install it or run from a project where it is available."
- If the returned major version is higher than **1** (i.e., 2.x, 3.x, …): warn the user —
  "This skill was written for openspec 1.x. The installed version is X.Y.Z — directory conventions may have changed. Check `.claude/commands/opsx/bdd.md` in the project for an updated copy."
  Then continue anyway (do not abort) unless the user stops you.

If a change name is provided, use it. Otherwise:
- Infer from conversation context
- Auto-select if only one active change exists
- If ambiguous, run `openspec list --json` and use **AskUserQuestion** to let the user select

Always announce: "Using change: `<name>`"

Check for `--force` flag — if present, overwrite existing files.

---

### 2. Detect project language and BDD framework

Inspect the project root to determine the language and BDD runner. Use the first match:

| Signal | Language | BDD runner | Feature dir | Step dir | Step ext |
|--------|----------|-----------|-------------|----------|----------|
| `package.json` + `playwright-bdd` in deps | TypeScript/JS | playwright-bdd | `e2e/features/` | `e2e/steps/` | `.steps.ts` / `.steps.js` |
| `package.json` (no playwright-bdd) + `.feature` files | TypeScript/JS | cucumber-js | `features/` | `step-definitions/` | `.steps.ts` / `.steps.js` |
| `pyproject.toml` / `setup.py` / `requirements*.txt` | Python | pytest-bdd or behave | `features/` | `features/steps/` (behave) or `tests/step_defs/` (pytest-bdd) | `.py` |
| `pom.xml` / `build.gradle` (Java) | Java | Cucumber JVM | `src/test/resources/features/` | `src/test/java/.../stepdefs/` | `.java` |
| `build.gradle.kts` / `build.gradle` (Kotlin) | Kotlin | Cucumber JVM | `src/test/resources/features/` | `src/test/kotlin/.../stepdefs/` | `.kt` |
| `go.mod` | Go | godog | `features/` | `features/` | `_test.go` |
| `Gemfile` | Ruby | Cucumber Ruby | `features/` | `features/step_definitions/` | `_steps.rb` |
| `*.csproj` / `*.sln` | C# | SpecFlow | `Features/` | `StepDefinitions/` | `Steps.cs` |

**If none of the above match:** ask the user which language/framework to use before continuing.

**Read existing BDD config** if present (e.g., `playwright.config.ts`, `behave.ini`, `cucumber.yml`) to confirm actual feature/step paths — they override the defaults in the table above.

Announce detected setup:
```
Language:    TypeScript
BDD runner:  playwright-bdd
Features:    e2e/features/
Steps:       e2e/steps/
```

---

### 3. Prerequisite checks (framework-specific)

Run the appropriate check for the detected runner:

**playwright-bdd:**
```bash
node -e "require('playwright-bdd')" 2>/dev/null && echo "PKG_OK" || echo "PKG_MISSING"
```
If `PKG_MISSING`: `npm install --save-dev playwright-bdd`

Check `playwright.config.ts` for `defineBddConfig`. If missing, add:
```ts
import { defineBddConfig } from 'playwright-bdd';
const bddTestDir = defineBddConfig({ features: './e2e/features/**/*.feature', steps: './e2e/steps/**/*.ts' });
```
And add platform projects to the `projects` array:
```ts
{ name: 'bdd-web', testDir: bddTestDir, grep: /@web/, use: { ...devices['Desktop Chrome'] } },
{ name: 'bdd-cli', testDir: bddTestDir, grep: /@cli/, use: {} },
{ name: 'bdd-api', testDir: bddTestDir, grep: /@api/, use: {} },
```

**cucumber-js:**
```bash
node -e "require('@cucumber/cucumber')" 2>/dev/null && echo "PKG_OK" || echo "PKG_MISSING"
```
If `PKG_MISSING`: `npm install --save-dev @cucumber/cucumber`

**pytest-bdd:**
```bash
python -c "import pytest_bdd" 2>/dev/null && echo "PKG_OK" || echo "PKG_MISSING"
```
If `PKG_MISSING`: `pip install pytest-bdd`

**behave:**
```bash
python -c "import behave" 2>/dev/null && echo "PKG_OK" || echo "PKG_MISSING"
```
If `PKG_MISSING`: `pip install behave`

**Cucumber JVM (Java/Kotlin):** check `pom.xml` or `build.gradle` for `io.cucumber` dependency. If missing, inform the user — do not auto-modify build files.

**godog:**
```bash
grep -r "godog" go.mod go.sum 2>/dev/null && echo "PKG_OK" || echo "PKG_MISSING"
```
If `PKG_MISSING`: `go get github.com/cucumber/godog/cmd/godog`

**Ensure feature and step directories exist:**
```bash
mkdir -p <feature-dir>/<name> <step-dir>
```

---

### 4. Discover spec files

```bash
find openspec/changes/<name>/specs -name "spec.md" | sort
```

If no spec files found: abort — "No spec files found in openspec/changes/<name>/specs/"

---

### 5. Check for existing output (without --force)

```bash
ls <feature-dir>/<name>/ 2>/dev/null
```

If files exist and `--force` is NOT set: abort with:
```
Feature files already exist for '<name>'. Use /opsx:bdd <name> --force to regenerate.
```

---

### 6. Generate feature files

For each spec file found:

**Read the spec file** and extract all scenarios with the pattern:
```markdown
#### Scenario: <title> [@platform]
- **WHEN** ...
- **THEN** ...
- **AND** ...
- **GIVEN** ... (if present)
```

**Platform tag rules:**
- If the scenario title contains `@web`, `@cli`, `@api`, `@android`, `@ios`, `@desktop` → use that tag
- If no platform tag → default to `@web`
- The platform tag appears on the line immediately before the `Scenario:` keyword

**Derive the spec name** from the path: `openspec/changes/<name>/specs/<spec-name>/spec.md` → `<spec-name>`

**Write** `<feature-dir>/<name>/<spec-name>.feature`:

```gherkin
# Generated by /opsx:bdd from openspec/changes/<name>/specs/<spec-name>/spec.md
# DO NOT EDIT — regenerate with /opsx:bdd <name> --force
Feature: <spec name in title case, dashes to spaces>

  Background:
    Given the application is available

  @<platform>
  Scenario: <title without @tag>
    When <WHEN step text>
    Then <THEN step text>
    And <AND step text>
```

Rules for step text:
- Strip the leading `**WHEN**`, `**THEN**`, `**AND**`, `**GIVEN**` marker
- Preserve the exact wording from the spec — do not paraphrase
- Map: `WHEN` → `When`, `THEN` → `Then`, `AND` → `And`, `GIVEN` → `Given`

**Background step wording:** Use a generic `Given the application is available` unless the project already has a Background step convention in existing feature files — in that case match it exactly.

---

### 7. Generate step stub files

Collect all unique steps across ALL spec files for this change, grouped by platform.

For each platform found, write one step file using the pattern for the detected language:

**TypeScript — playwright-bdd** (`<step-dir>/<name>.<platform>.steps.ts`):
```ts
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

// ── Background ────────────────────────────────────────────────────────────────

Given('the application is available', async ({ page, baseURL }) => {
  // configure as needed
});

// ── <spec-name>: <Scenario title> ─────────────────────────────────────────────

When('<step text>', async ({ page }) => {
  throw new Error('Not implemented');
});

Then('<step text>', async ({ page }) => {
  throw new Error('Not implemented');
});
```
Use `async ({ page }) => {` for `@web`; `async () => {` for `@cli`/`@api`.

**TypeScript — cucumber-js** (`<step-dir>/<name>.<platform>.steps.ts`):
```ts
import { Given, When, Then } from '@cucumber/cucumber';

Given('the application is available', async function() {
  // configure as needed
});

When('<step text>', async function() {
  throw new Error('Not implemented');
});

Then('<step text>', async function() {
  throw new Error('Not implemented');
});
```

**Python — pytest-bdd** (`<step-dir>/test_<name>_<platform>.py`):
```python
import pytest
from pytest_bdd import given, when, then, scenarios

scenarios('../features/<name>/<spec-name>.feature')

@given('the application is available')
def application_available():
    pass  # configure as needed

@when('<step text>')
def step_when():
    raise NotImplementedError('Not implemented')

@then('<step text>')
def step_then():
    raise NotImplementedError('Not implemented')
```

**Python — behave** (`<step-dir>/<name>_<platform>_steps.py`):
```python
from behave import given, when, then

@given('the application is available')
def step_impl(context):
    pass  # configure as needed

@when('<step text>')
def step_impl(context):
    raise NotImplementedError('Not implemented')

@then('<step text>')
def step_impl(context):
    raise NotImplementedError('Not implemented')
```

**Java — Cucumber JVM** (`<step-dir>/<NamePlatform>Steps.java`):
```java
import io.cucumber.java.en.*;

public class <NamePlatform>Steps {

    @Given("the application is available")
    public void theApplicationIsAvailable() {
        // configure as needed
    }

    @When("<step text>")
    public void <camelCaseMethod>() {
        throw new io.cucumber.java.PendingException();
    }

    @Then("<step text>")
    public void <camelCaseMethod>() {
        throw new io.cucumber.java.PendingException();
    }
}
```

**Kotlin — Cucumber JVM** (`<step-dir>/<NamePlatform>Steps.kt`):
```kotlin
import io.cucumber.java.en.*

class <NamePlatform>Steps {

    @Given("the application is available")
    fun theApplicationIsAvailable() {
        // configure as needed
    }

    @When("<step text>")
    fun <camelCaseMethod>() {
        throw io.cucumber.java.PendingException()
    }

    @Then("<step text>")
    fun <camelCaseMethod>() {
        throw io.cucumber.java.PendingException()
    }
}
```

**Go — godog** (`<feature-dir>/<name>/<name>_<platform>_test.go`):
```go
package <name>_test

import (
    "github.com/cucumber/godog"
    "testing"
)

func theApplicationIsAvailable() error {
    return nil // configure as needed
}

func <camelCaseStep>() error {
    return godog.ErrPending
}

func InitializeScenario(ctx *godog.ScenarioContext) {
    ctx.Given(`the application is available`, theApplicationIsAvailable)
    ctx.When(`<step text>`, <camelCaseStep>)
    ctx.Then(`<step text>`, <camelCaseStep>)
}

func Test<Name>(t *testing.T) {
    suite := godog.TestSuite{
        ScenarioInitializer: InitializeScenario,
        Options: &godog.Options{Format: "pretty", Paths: []string{"."}, TestingT: t},
    }
    if suite.Run() != 0 { t.Fatal("BDD tests failed") }
}
```

**Ruby — Cucumber** (`<step-dir>/<name>_<platform>_steps.rb`):
```ruby
Given('the application is available') do
  # configure as needed
end

When('<step text>') do
  pending # Not implemented
end

Then('<step text>') do
  pending # Not implemented
end
```

**C# — SpecFlow** (`<step-dir>/<NamePlatform>Steps.cs`):
```csharp
using TechTalk.SpecFlow;

[Binding]
public class <NamePlatform>Steps
{
    [Given("the application is available")]
    public void TheApplicationIsAvailable() { }

    [When("<step text>")]
    public void <PascalCaseMethod>()
    {
        throw new PendingStepException();
    }

    [Then("<step text>")]
    public void <PascalCaseMethod>()
    {
        throw new PendingStepException();
    }
}
```

**General rules for all languages:**
- One comment/section header per scenario group
- Background step is always first and is NOT a stub
- Deduplicate: emit each unique step text only once
- Preserve exact step wording from the feature file

---

### 8. Verify generated files

Run the framework-appropriate parse/dry-run check:

| Framework | Verification command |
|-----------|----------------------|
| playwright-bdd | `npx bddgen 2>&1` |
| cucumber-js | `npx cucumber-js --dry-run 2>&1` |
| pytest-bdd | `python -m pytest --collect-only 2>&1 \| head -30` |
| behave | `python -m behave --dry-run 2>&1` |
| Cucumber JVM | `mvn test-compile 2>&1` or `./gradlew testClasses 2>&1` |
| godog | `go build ./... 2>&1` |
| Cucumber Ruby | `bundle exec cucumber --dry-run 2>&1` |
| SpecFlow | `dotnet build 2>&1` |

- If it passes: proceed
- If it fails: show the error, fix the offending file, retry once

**Do NOT run the full test suite** — tests will be RED/pending and that is expected.

---

### 9. Show summary

```
## BDD Generated: <name>

Language:   <language>
Runner:     <framework>

Feature files:
  <feature-dir>/<name>/
    ✓ <spec-name>.feature  (N scenarios)
    ✓ <spec-name>.feature  (N scenarios)

Step files:
  <step-dir>/<name>.<platform>.<ext>  (N steps)

Total: N scenarios · all RED ✓ (parse check: OK)

Next: /opsx:apply-bdd <name> to implement — BDD tests gate each task
```

---

## Guardrails

- Never overwrite existing feature files unless `--force` is passed
- Detect the project language before generating — never assume TypeScript
- Preserve exact step wording from the spec — do not rephrase or summarise
- Default platform tag to `@web` if none is specified in the spec
- Background step is the only non-stub — all other steps must be pending/throw
- Do NOT run the full test suite — RED/pending tests are the expected starting state
- If an existing step convention is already in the project (e.g., shared Background), match it
