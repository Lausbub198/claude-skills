// Scroll reveal — paste verbatim before </body>
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting) requestAnimationFrame(() => e.target.classList.add('in'))
  })
}, {threshold: 0, rootMargin: '0px 0px -60px 0px'})
document.querySelectorAll('.reveal,.reveal-l,.reveal-r').forEach(el => io.observe(el))

// Phase nav active state — update section IDs to match your page
const sections = ['s0','s1','s2','s3','s4','s5','s6','s7','s8']
const dots = document.querySelectorAll('.pn-dot')
const sectionEls = sections.map(id => document.getElementById(id))

const navObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting) {
      const idx = sectionEls.indexOf(e.target)
      if(idx >= 0) {
        dots.forEach(d => d.classList.remove('active'))
        dots[idx].classList.add('active')
      }
    }
  })
}, {threshold: 0.4})
sectionEls.forEach(el => { if(el) navObs.observe(el) })
