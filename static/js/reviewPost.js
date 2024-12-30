const reviewTitleForm = document.querySelector('#review_title')
const reviewContentForm = document.querySelector('#review_content')

const inputTitleWrap = document.querySelector('#inputTitleWrap')
const inputContentWrap = document.querySelector('#inputContentWrap')

if (reviewTitleForm != null) {
  reviewTitleForm.addEventListener("input", function(e) {
    inputTitleWrap.setAttribute("data-length", e.target.value.length + "/30")
  })
}
if (reviewContentForm != null) {
  reviewContentForm.addEventListener("input", function(e) {
    inputContentWrap.setAttribute("data-length", e.target.value.length + "/320,000")
  })
}
