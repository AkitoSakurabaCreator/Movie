const searchFormArea = document.querySelector('.search_formarea')
const searchForm = document.querySelector('.search_form')
const searchButton = document.querySelector('.search_formarea button')

const header = document.querySelector('header')

if (window.innerWidth < 480 ) {
  searchButton.addEventListener("click", function(e) {
    e.preventDefault()
    const searchModalSp = document.createElement("div")
    searchModalSp.classList.add("searchModalSp")
    const headerModalContent = document.createElement("div")
    headerModalContent.classList.add("headerModalContent")
    searchModalSp.appendChild(headerModalContent)

    const searchFormAreaClone = searchFormArea.cloneNode(true);
    headerModalContent.appendChild(searchFormAreaClone)

    const closeButton = document.createElement("span")
    closeButton.classList.add("closeButton")
    closeButton.textContent = "×"
    headerModalContent.appendChild(closeButton)

    header.appendChild(searchModalSp)

    searchModalSp.querySelector(".closeButton").addEventListener("click", function(e) {
      searchModalSp.remove()
    })
  
    searchModalSp.addEventListener("click", function() {
      searchModalSp.remove()
    });
    
    headerModalContent.addEventListener("click", function(e) {
      e.stopPropagation()
    });
  })

  searchFormArea.addEventListener("keypress", function(e) {
    if (e.key === "Enter" || e.keyCode === 13) {
      e.preventDefault()
      searchFormArea.submit()
    }
  })
}
