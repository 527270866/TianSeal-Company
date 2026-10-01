// Catalog rendering and shared interactions.
const pageLang = (document.documentElement.lang || "en").toLowerCase();
const locale = pageLang.startsWith("zh") ? "zh" : pageLang.startsWith("es") ? "es" : "en";
const imagePrefix = document.documentElement.dataset.imagePrefix || "";

const UI = {
  en: {
    view: "View", factoryModel: "Factory model", specialSourcing: "Special sourcing", byRequest: "BY REQUEST", viewProduct: "View product →", quote: "Quote",
    noMatch: "No matching model found. Try a different product code.",
    desc: (m) => `Factory model ${m} from the Tianseal International Inc security seal catalog. Open the product page to view the supplied factory image and request current verified specifications.`,
    specialDesc: (m) => `Special-sourcing model ${m} available by request. Current source, specifications, MOQ, lead time and availability are confirmed for each order.`,
    series: {"H Series":"H Series","FP Series":"FP Series","P Series":"P Series","Other Models":"Other Models"}
  },
  zh: {
    view: "查看", factoryModel: "工厂型号", specialSourcing: "特殊采购", byRequest: "按需供应", viewProduct: "查看产品 →", quote: "询价",
    noMatch: "未找到匹配型号，请尝试其他产品编号。",
    desc: (m) => `Tianseal International Inc 安全封条目录中的工厂型号 ${m}。打开产品页面可查看工厂原图，并咨询当前确认后的规格。`,
    specialDesc: (m) => `型号 ${m} 为特殊采购产品，可按项目需求供应。当前供应来源、规格、MOQ、交期和可供情况将在每次询价时确认。`,
    series: {"H Series":"H 系列","FP Series":"FP 系列","P Series":"P 系列","Other Models":"其他型号"}
  },
  es: {
    view: "Ver", factoryModel: "Modelo de fábrica", specialSourcing: "Abastecimiento especial", byRequest: "BAJO SOLICITUD", viewProduct: "Ver producto →", quote: "Cotizar",
    noMatch: "No se encontró un modelo coincidente. Pruebe con otro código de producto.",
    desc: (m) => `Modelo de fábrica ${m} del catálogo de sellos de seguridad de Tianseal International Inc. Abra la página del producto para ver la imagen de fábrica y solicitar especificaciones vigentes verificadas.`,
    specialDesc: (m) => `El modelo ${m} se ofrece mediante abastecimiento especial. La fuente actual, especificaciones, MOQ, plazo y disponibilidad se confirman para cada pedido.`,
    series: {"H Series":"Serie H","FP Series":"Serie FP","P Series":"Serie P","Other Models":"Otros modelos"}
  }
}[locale];

const productGrid = document.getElementById("productGrid");
const productSelect = document.getElementById("productSelect");
const productSearch = document.getElementById("productSearch");
const visibleProductCount = document.getElementById("visibleProductCount");
const catalogEmpty = document.getElementById("catalogEmpty");
const filterButtons = [...document.querySelectorAll(".catalog-filter")];
let activeSeries = "all";
let searchTerm = "";

function filteredProducts() {
  return products.filter((product) => {
    const seriesMatch = activeSeries === "all" || product.series === activeSeries;
    const haystack = `${product.model} ${product.title} ${product.series} ${product.category}`.toLowerCase();
    const searchMatch = !searchTerm || haystack.includes(searchTerm);
    return seriesMatch && searchMatch;
  });
}
function renderProducts() {
  if (!productGrid) return;
  const list = filteredProducts();
  productGrid.innerHTML = list.map((product) => `
    <article class="product-card reveal visible">
      <a class="product-card-image-link" href="${product.detailPage}" aria-label="${UI.view} ${product.model}">
        <div class="product-art catalog-product">
          <img src="${imagePrefix}${product.image}" alt="${product.model} product image" loading="lazy">
          <span class="product-series-chip">${UI.series[product.series] || product.series}</span>
          ${product.sourceType === "special" ? `<span class="product-source-chip">${UI.byRequest}</span>` : ""}
        </div>
      </a>
      <div class="product-meta"><span class="tag">${product.sourceType === "special" ? UI.specialSourcing : UI.factoryModel}</span><span class="model">${product.model}</span></div>
      <h3>${product.model}</h3>
      <p>${product.sourceType === "special" ? UI.specialDesc(product.model) : UI.desc(product.model)}</p>
      <div class="product-card-actions">
        <a class="text-link product-detail-link" href="${product.detailPage}">${UI.viewProduct}</a>
        <a class="quote-mini-link" href="?product=${encodeURIComponent(product.id)}#contact">${UI.quote}</a>
      </div>
    </article>`).join("");
  if (visibleProductCount) visibleProductCount.textContent = list.length;
  if (catalogEmpty) { catalogEmpty.hidden = list.length !== 0; catalogEmpty.textContent = UI.noMatch; }
}
function populateProductSelect() {
  if (!productSelect) return;
  const otherOption = productSelect.querySelector('option[value="other"]');
  products.forEach((product) => {
    const option = document.createElement("option");
    option.value = product.id;
    option.textContent = product.model;
    productSelect.insertBefore(option, otherOption);
  });
  const requestedProduct = new URLSearchParams(window.location.search).get("product");
  if (requestedProduct && products.some((p) => p.id === requestedProduct)) productSelect.value = requestedProduct;
}
productSearch?.addEventListener("input", (event) => { searchTerm = event.target.value.trim().toLowerCase(); renderProducts(); });
filterButtons.forEach((button) => button.addEventListener("click", () => {
  activeSeries = button.dataset.series;
  filterButtons.forEach((b) => b.classList.toggle("active", b === button));
  renderProducts();
}));
populateProductSelect(); renderProducts();

const menuButton = document.querySelector(".menu-button");
const mainNav = document.querySelector(".main-nav");
if (menuButton && mainNav) {
  menuButton.addEventListener("click", () => {
    const isOpen = mainNav.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", isOpen);
  });
  document.querySelectorAll(".main-nav a").forEach((link) => link.addEventListener("click", () => {
    mainNav.classList.remove("open"); menuButton.setAttribute("aria-expanded", "false");
  }));
}
const year = document.getElementById("year"); if (year) year.textContent = new Date().getFullYear();
const revealItems = document.querySelectorAll(".reveal");
const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
  if (entry.isIntersecting) { entry.target.classList.add("visible"); observer.unobserve(entry.target); }
}), { threshold: 0.12 });
revealItems.forEach((item) => observer.observe(item));
