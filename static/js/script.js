document.addEventListener("DOMContentLoaded", function () {
  /* ---------------- Page Loader / Curtain ---------------- */
  window.addEventListener("load", function () {
    setTimeout(function () { document.body.classList.add("loaded"); }, 400);
  });
  setTimeout(function () { document.body.classList.add("loaded"); }, 2200); // fail-safe

  /* ---------------- AOS ---------------- */
  if (window.AOS) {
    AOS.init({ duration: 900, once: true, offset: 80, easing: "ease-out-cubic" });
  }

  /* ---------------- Swipe-up Section Reveal ---------------- */
  const swipeSections = document.querySelectorAll("main > section:not(.hero):not(.page-hero)");
  if (swipeSections.length && "IntersectionObserver" in window) {
    swipeSections.forEach(sec => sec.classList.add("swipe-reveal"));
    const swipeObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("swipe-in");
          swipeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: "0px 0px -10% 0px" });
    swipeSections.forEach(sec => swipeObserver.observe(sec));
  }

  /* ---------------- Custom Cursor ---------------- */
  const cursorDot = document.getElementById("cursor-dot");
  const cursorRing = document.getElementById("cursor-ring");
  if (cursorDot && cursorRing && window.matchMedia("(hover: hover)").matches) {
    let ringX = 0, ringY = 0, mouseX = 0, mouseY = 0;
    document.addEventListener("mousemove", function (e) {
      mouseX = e.clientX; mouseY = e.clientY;
      cursorDot.style.left = mouseX + "px";
      cursorDot.style.top = mouseY + "px";
    });
    (function animateRing() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      cursorRing.style.left = ringX + "px";
      cursorRing.style.top = ringY + "px";
      requestAnimationFrame(animateRing);
    })();
    document.querySelectorAll("a, button, input, textarea, select, .magnetic").forEach(function (el) {
      el.addEventListener("mouseenter", () => cursorRing.classList.add("cursor-active"));
      el.addEventListener("mouseleave", () => cursorRing.classList.remove("cursor-active"));
    });
  }

  /* ---------------- Magnetic Buttons ---------------- */
  document.querySelectorAll(".magnetic").forEach(function (el) {
    el.addEventListener("mousemove", function (e) {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      el.style.transform = `translate(${x * 0.18}px, ${y * 0.35}px)`;
    });
    el.addEventListener("mouseleave", function () { el.style.transform = "translate(0,0)"; });
  });

  /* ---------------- Scroll Progress + Header + Back To Top ---------------- */
  const progressBar = document.getElementById("scroll-progress-bar");
  const header = document.getElementById("site-header");
  const backToTop = document.getElementById("back-to-top");
  window.addEventListener("scroll", function () {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = pct + "%";
    if (header) header.classList.toggle("scrolled", scrollTop > 30);
    if (backToTop) backToTop.classList.toggle("show", scrollTop > 500);
  }, { passive: true });
  if (backToTop) {
    backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  /* ---------------- Nav Toggle ---------------- */
  const navToggle = document.getElementById("nav-toggle");
  const mainNav = document.getElementById("main-nav");
  if (navToggle && mainNav) {
    navToggle.addEventListener("click", function () {
      mainNav.classList.toggle("open");
      navToggle.classList.toggle("open");
    });
    mainNav.querySelectorAll("a").forEach(a => a.addEventListener("click", () => mainNav.classList.remove("open")));
  }

  /* ---------------- Nav Search Expand (mobile tap) ---------------- */
  document.querySelectorAll(".nav-search").forEach(function (form) {
    form.addEventListener("click", function () { form.classList.add("active"); });
  });

  /* ---------------- Profile Dropdown ---------------- */
  const profileMenu = document.querySelector(".profile-menu");
  const profileToggle = document.getElementById("profile-toggle");
  if (profileToggle && profileMenu) {
    profileToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      profileMenu.classList.toggle("open");
    });
    document.addEventListener("click", function () { profileMenu.classList.remove("open"); });
  }

  /* ---------------- Dark Mode Toggle ---------------- */
  const darkToggle = document.getElementById("dark-mode-toggle");
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("karma-theme");
  if (savedTheme === "dark") {
    root.setAttribute("data-theme", "dark");
  }
  if (darkToggle) {
    darkToggle.addEventListener("click", function () {
      const isDark = root.getAttribute("data-theme") === "dark";
      if (isDark) {
        root.removeAttribute("data-theme");
        localStorage.setItem("karma-theme", "light");
      } else {
        root.setAttribute("data-theme", "dark");
        localStorage.setItem("karma-theme", "dark");
      }
    });
  }

  /* ---------------- Flash Toast Auto Dismiss ---------------- */
  document.querySelectorAll(".flash-toast").forEach(function (toast) {
    const closeBtn = toast.querySelector(".flash-close");
    if (closeBtn) closeBtn.addEventListener("click", () => toast.remove());
    setTimeout(() => toast.remove(), 6000);
  });

  /* ---------------- Animated Counters ---------------- */
  const counters = document.querySelectorAll(".counter-num[data-count]");
  if (counters.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(c => observer.observe(c));
  }
  function animateCounter(el) {
    const target = parseInt(el.getAttribute("data-count"), 10);
    const suffix = el.getAttribute("data-suffix") || "";
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    const timer = setInterval(function () {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = current + suffix;
    }, 25);
  }

  /* ---------------- Parallax Hero ---------------- */
  const heroBg = document.querySelector(".hero-bg");
  if (heroBg) {
    window.addEventListener("scroll", function () {
      const offset = window.scrollY;
      if (offset < window.innerHeight) {
        heroBg.style.transform = `translateY(${offset * 0.35}px) scale(1.05)`;
      }
    }, { passive: true });
  }

  /* ---------------- Split Text Reveal ---------------- */
  document.querySelectorAll(".split-text").forEach(function (el) {
    const words = el.textContent.trim().split(" ");
    el.innerHTML = words.map((w, i) => `<span style="animation-delay:${i * 0.06}s">${w}&nbsp;</span>`).join("");
  });

  /* ---------------- Spice Particles ---------------- */
  document.querySelectorAll(".spice-particles").forEach(function (container) {
    for (let i = 0; i < 22; i++) {
      const p = document.createElement("span");
      p.className = "spice-particle";
      p.style.left = Math.random() * 100 + "%";
      p.style.animationDuration = 6 + Math.random() * 10 + "s";
      p.style.animationDelay = Math.random() * 8 + "s";
      p.style.width = p.style.height = (3 + Math.random() * 4) + "px";
      container.appendChild(p);
    }
  });

  /* ---------------- Swiper Sliders ---------------- */
  if (window.Swiper) {
    if (document.querySelector(".testimonial-swiper")) {
      new Swiper(".testimonial-swiper", {
        loop: true, autoplay: { delay: 5000 }, pagination: { el: ".swiper-pagination", clickable: true },
      });
    }
    if (document.querySelector(".chef-swiper")) {
      new Swiper(".chef-swiper", {
        slidesPerView: 1.15, spaceBetween: 24, loop: true, autoplay: { delay: 4200 },
        breakpoints: { 768: { slidesPerView: 2.2 }, 1100: { slidesPerView: 3.2 } },
      });
    }
    if (document.querySelector(".gallery-preview-swiper")) {
      new Swiper(".gallery-preview-swiper", {
        slidesPerView: 1.2, spaceBetween: 18, loop: true, autoplay: { delay: 3600 },
        breakpoints: { 640: { slidesPerView: 2.3 }, 1000: { slidesPerView: 3.5 } },
      });
    }
  }

  /* ---------------- Menu Category Filter (instant client filter, form also works without JS) ---------------- */
  document.querySelectorAll(".filter-chip[data-category]").forEach(function (chip) {
    chip.addEventListener("click", function (e) {
      // Native navigation handled via href; this just adds active state pre-nav for smoothness
      document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
    });
  });

  /* ---------------- Gallery Lightbox ---------------- */
  const lightbox = document.getElementById("lightbox");
  if (lightbox) {
    const lbImg = lightbox.querySelector("img");
    const items = Array.from(document.querySelectorAll(".masonry-item img"));
    let currentIndex = 0;

    function openLightbox(index) {
      currentIndex = index;
      lbImg.src = items[currentIndex].src;
      lbImg.alt = items[currentIndex].alt;
      lightbox.classList.add("active");
    }
    document.querySelectorAll(".masonry-item").forEach(function (item, index) {
      item.addEventListener("click", () => openLightbox(index));
    });
    lightbox.querySelector(".lightbox-close").addEventListener("click", () => lightbox.classList.remove("active"));
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.classList.remove("active"); });
    lightbox.querySelector(".lightbox-next").addEventListener("click", function () {
      currentIndex = (currentIndex + 1) % items.length; openLightbox(currentIndex);
    });
    lightbox.querySelector(".lightbox-prev").addEventListener("click", function () {
      currentIndex = (currentIndex - 1 + items.length) % items.length; openLightbox(currentIndex);
    });
    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("active")) return;
      if (e.key === "Escape") lightbox.classList.remove("active");
      if (e.key === "ArrowRight") lightbox.querySelector(".lightbox-next").click();
      if (e.key === "ArrowLeft") lightbox.querySelector(".lightbox-prev").click();
    });
  }

  /* ---------------- CSRF Helper ---------------- */
  function getCsrfToken() {
    const meta = document.querySelector('input[name="csrf_token"]');
    return meta ? meta.value : "";
  }

  /* ---------------- Cart Count Init ---------------- */
  function refreshCartCountFromStorage() {
    const el = document.getElementById("cart-count");
    if (el && window.__cartCount !== undefined) el.textContent = window.__cartCount;
  }
  refreshCartCountFromStorage();

  /* ---------------- Add To Cart ---------------- */
  document.querySelectorAll(".add-cart-btn[data-item-id]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const itemId = btn.getAttribute("data-item-id");
      fetch("/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrfToken() },
        body: JSON.stringify({ item_id: itemId, qty: 1 }),
      })
        .then(r => r.json())
        .then(function (data) {
          if (data.ok) {
            const countEl = document.getElementById("cart-count");
            if (countEl) countEl.textContent = data.cart_count;
            showMiniToast(data.message);
          }
        });
    });
  });

  function showMiniToast(message) {
    const wrap = document.getElementById("flash-wrap");
    if (!wrap) return;
    const toast = document.createElement("div");
    toast.className = "flash-toast flash-success";
    toast.innerHTML = `<span>${message}</span><button class="flash-close">&times;</button>`;
    wrap.appendChild(toast);
    toast.querySelector(".flash-close").addEventListener("click", () => toast.remove());
    setTimeout(() => toast.remove(), 3500);
  }

  /* ---------------- Cart Qty +/- (on cart/order page) ---------------- */
  document.querySelectorAll(".qty-control").forEach(function (control) {
    const itemId = control.getAttribute("data-item-id");
    const display = control.querySelector(".qty-display");
    control.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        let qty = parseInt(display.textContent, 10);
        qty = btn.classList.contains("qty-plus") ? qty + 1 : qty - 1;
        if (qty < 0) qty = 0;
        fetch("/cart/update", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrfToken() },
          body: JSON.stringify({ item_id: itemId, qty: qty }),
        })
          .then(r => r.json())
          .then(function (data) {
            if (data.ok) { window.location.reload(); }
          });
      });
    });
  });

  document.querySelectorAll(".cart-remove-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      fetch("/cart/remove", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrfToken() },
        body: JSON.stringify({ item_id: btn.getAttribute("data-item-id") }),
      }).then(() => window.location.reload());
    });
  });

  /* ---------------- Coupon Apply ---------------- */
  const couponForm = document.getElementById("coupon-form");
  if (couponForm) {
    couponForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const code = couponForm.querySelector("input[name=coupon_code]").value;
      fetch("/cart/apply-coupon", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrfToken() },
        body: JSON.stringify({ coupon_code: code }),
      })
        .then(r => r.json())
        .then(function (data) {
          const msgEl = document.getElementById("coupon-msg");
          if (msgEl) {
            msgEl.textContent = data.message;
            msgEl.style.color = data.ok ? "#1c7d3a" : "#c0392b";
          }
          if (data.ok) {
            const discountEl = document.getElementById("summary-discount");
            const taxEl = document.getElementById("summary-tax");
            const totalEl = document.getElementById("summary-total");
            if (discountEl) discountEl.textContent = "-$" + data.discount.toFixed(2);
            if (taxEl) taxEl.textContent = "$" + data.tax.toFixed(2);
            if (totalEl) totalEl.textContent = "$" + data.total.toFixed(2);
          }
        });
    });
  }

  /* ---------------- Newsletter ---------------- */
  const newsletterForm = document.getElementById("newsletter-form");
  if (newsletterForm) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const email = newsletterForm.querySelector("input[name=email]").value;
      const msg = document.getElementById("newsletter-msg");
      fetch("/newsletter/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrfToken() },
        body: JSON.stringify({ email: email }),
      })
        .then(r => r.json())
        .then(function (data) {
          if (msg) msg.textContent = data.message;
          if (data.ok) newsletterForm.reset();
        });
    });
  }

  /* ---------------- Payment Method: show Stripe info panel + update submit label ---------------- */
  const paymentSelect = document.getElementById("payment_method");
  const cardPanel = document.getElementById("card-payment-panel");
  const submitBtn = document.getElementById("checkout-submit-btn");
  const submitBtnBaseLabel = submitBtn ? submitBtn.innerHTML : "";

  function isStripeSelected() {
    return paymentSelect && paymentSelect.value === "Pay Online (Card via Stripe)";
  }

  function toggleCardPanel() {
    if (cardPanel) cardPanel.style.display = isStripeSelected() ? "block" : "none";
    if (submitBtn) {
      submitBtn.innerHTML = isStripeSelected()
        ? '<i class="bi bi-shield-lock"></i> Continue to Secure Payment'
        : submitBtnBaseLabel;
    }
  }
  if (paymentSelect) {
    paymentSelect.addEventListener("change", toggleCardPanel);
    toggleCardPanel();
  }

  /* ---------------- Order Type Toggle (delivery address show/hide) ---------------- */
  const orderTypeSelect = document.getElementById("order_type");
  const addressGroup = document.getElementById("delivery-address-group");
  function toggleAddress() {
    if (!orderTypeSelect || !addressGroup) return;
    addressGroup.style.display = orderTypeSelect.value === "delivery" ? "flex" : "none";
  }
  if (orderTypeSelect) {
    orderTypeSelect.addEventListener("change", toggleAddress);
    toggleAddress();
  }

  /* ---------------- Reservation min date = today ---------------- */
  const dateInput = document.getElementById("date");
  if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("min", today);
  }
});
