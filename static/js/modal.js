const modal = document.getElementById('easyModal');
const buttonClose = document.getElementsByClassName('modalClose')[0];

const hostUrl = "http://" + location.host

// バツ印がクリックされた時
buttonClose.addEventListener('click', modalClose);
function modalClose() {
    modal.style.visibility = 'hidden';
    history.replaceState("", "", hostUrl)
}

// モーダルコンテンツ以外がクリックされた時
addEventListener('click', outsideClose);
function outsideClose(e) {
    if (e.target == modal) {
    modal.style.visibility = 'hidden';
    }
}

let modalHeader = document.querySelector('.modal-header')

let modal_body = document.querySelector(".modal-body")
let clickDetail = document.querySelectorAll('.clickDetail')
let modalFunction = document.querySelector('.modal_function')
let castDiv = document.querySelector(".cast_list")

let movieBackground = document.querySelector('.movieBackground')
let moviePoster = document.querySelector('.moviePoster')
let genre_list = document.querySelector('.genre_list')
let modal_title = document.querySelector('.modal_title')
let modal_date = document.querySelector('.modal_date')
let languageList = document.querySelector('.languageList')
let video = document.querySelector('.video')
let modal_review = document.querySelector('.modal_review')

let reviewStars = document.querySelector('.reviewStars')
let review_post = document.querySelector('.review_post')
let overviewContainer = document.querySelector('.overviewContainer')
let overview = document.querySelector('.overview')

let similar_list = document.querySelector('.similar_list')

let homepage = document.querySelector('#homepage')
let mylist = document.querySelector('#mylist')
let review = document.querySelector('#review')

var reviewCount = 1;
const reviewList = document.querySelector('.reviewList')

let reviewButton = document.querySelector('#reviewButton')
let reviewContinue = document.querySelector('#review')

let reviewContent = document.querySelector('.reviewContent')

let myListButton = document.querySelector('.myListButton')
let myListSwitch = false
let copyButton = document.querySelector('#copyClipboard')

var endSwitch = "true";
var movieId = ""


function reviewComment(){
    $.ajax({
    'url': 'review',
    'type': 'GET',
    'data': {
        'page': reviewCount,
        'movie_id': movieId
    },
    'dataType': 'json'
})
.done(function(response){
    userReview = response.userReview
    if (userReview != "false"){
        const list = document.createElement('li')

        const reviewerDiv = document.createElement('div')
        reviewerDiv.classList.add('reviewer')
        const userImage = document.createElement('img')
        userImage.src = userReview.avatar

        const userNameContainer = document.createElement('div')
        const nameP = document.createElement('p')
        if (window.innerWidth < 480) {
            if (userReview.name.length > 6) {
                userReview.name = userReview.name.substring(0, 6) + '––––';
            }
        } else {
            if (userReview.name.length > 16) {
                userReview.name = userReview.name.substring(0, 16) + '––––';
            }
            if (userReview.screen.length > 16) {
                userReview.screen = userReview.screen.substring(0, 16) + '––––';
            }
        }
        nameP.textContent = userReview.name
        const screenP = document.createElement('p')
        screenP.textContent = userReview.screen

        userNameContainer.appendChild(nameP)
        userNameContainer.appendChild(screenP)
        reviewerDiv.appendChild(userImage)
        reviewerDiv.appendChild(userNameContainer)

        // console.log(userReview.like)
        const reviewFlexContainer = document.createElement('div')
        reviewFlexContainer.classList.add('reviewFlexContainer')
        const likeDiv = document.createElement('div')
        likeDiv.classList.add('likeStarContainer')
        for (let i = 0; i < userReview.like; i++) {
            const likeImage = document.createElement('img')
            likeImage.src = "/static/images/starFill-24.svg"
            likeDiv.appendChild(likeImage)
        }
        reviewFlexContainer.appendChild(reviewerDiv)
        reviewFlexContainer.appendChild(likeDiv)

        const titleP = document.createElement('p')
        titleP.classList.add('reviewTitle')
        titleP.textContent = userReview.title
        const contentP = document.createElement('p')
        contentP.classList.add('reviewContent')
        contentP.textContent = userReview.content

        const reviewFunctionP = document.createElement('p')
        reviewFunctionP.classList.add('reviewFunction')

        const a = document.createElement('a')
        a.href = "/review_edit/" + userReview.id

        const editI = document.createElement('i')
        editI.classList.add('fa-solid', 'fa-pen-to-square')
        editI.textContent = '編集'

        a.appendChild(editI)
        reviewFunctionP.appendChild(a)
        list.appendChild(reviewFlexContainer);
        list.appendChild(titleP)
        list.appendChild(contentP)
        list.appendChild(reviewFunctionP)
        reviewList.appendChild(list)
    }
    
    console.log(response.reviews);
    for (const review of response.reviews) {
        const reviewFunction = document.querySelector('.reviewFunction')
        console.log(reviewFunction)
        let filter = 'blur(4px)'

        const list = document.createElement('li')

        const reviewerDiv = document.createElement('div')
        reviewerDiv.classList.add('reviewer')
        const userImage = document.createElement('img')
        userImage.src = review.avatar

        const userNameContainer = document.createElement('div')
        const nameP = document.createElement('p')
        if (window.innerWidth < 480) {
            if (review.name.length > 6) {
                review.name = review.name.substring(0, 6) + '––––';
            }
        } else {
            if (review.name.length > 16) {
                review.name = review.name.substring(0, 16) + '.––––';
            }
            if (review.screen.length > 16) {
                review.screen = review.screen.substring(0, 16) + '––––';
            }
        }
        nameP.textContent = review.name
        const screenP = document.createElement('p')
        screenP.textContent = review.screen

        userNameContainer.appendChild(nameP)
        userNameContainer.appendChild(screenP)
        reviewerDiv.appendChild(userImage)
        reviewerDiv.appendChild(userNameContainer)

        const reviewFlexContainer = document.createElement('div')
        reviewFlexContainer.classList.add('reviewFlexContainer')
        const likeDiv = document.createElement('div')
        likeDiv.classList.add('likeStarContainer')
        for (let i = 0; i < review.like; i++) {
            const likeImage = document.createElement('img')
            likeImage.src = "/static/images/starFill-24.svg"
            likeDiv.appendChild(likeImage)
        }
        reviewFlexContainer.appendChild(reviewerDiv)
        reviewFlexContainer.appendChild(likeDiv)

        const titleP = document.createElement('p')
        titleP.classList.add('reviewTitle')
        titleP.textContent = review.title
        const contentP = document.createElement('p')
        contentP.classList.add('reviewContentIgnoreMe')
        contentP.textContent = review.content

        const reviewFunctionOthersP = document.createElement('p')
        reviewFunctionOthersP.classList.add('reviewFunctionOthers')

        list.appendChild(reviewFlexContainer);
        list.appendChild(titleP)
        list.appendChild(contentP)
        list.appendChild(reviewFunctionOthersP)
        reviewList.appendChild(list)

        console.log(review)
        console.log(review.name, review.screen, review.title, review.like, review.content, review.spoiler, review.avatar)

        const cancelBlurSpan = document.createElement('span')
        cancelBlurSpan.classList.add('cancelBlur')
        const eye = document.createElement('i')
        eye.classList.add('fa-solid', 'fa-eye-slash')
        
        eye.textContent = 'ネタバレ'
        cancelBlurSpan.appendChild(eye)
        reviewFunctionOthersP.prepend(cancelBlurSpan)

        if (review.spoiler == true) {
            filter = 'blur(4px)'
            eye.classList.replace('fa-eye', 'fa-eye-slash')
        } else {
            filter = 'none'
            eye.classList.replace('fa-eye-slash', 'fa-eye')
        }
        contentP.style.filter = filter

        cancelBlurSpan.addEventListener("click", function() {
            console.log(reviewFunctionOthersP)
            if (review.spoiler != true) {
                filter = 'blur(4px)'
                eye.classList.replace('fa-eye', 'fa-eye-slash')
            } else {
                filter = 'none'
                eye.classList.replace('fa-eye-slash', 'fa-eye')
            }
            contentP.style.filter = filter
            review.spoiler = !review.spoiler
        });
    }
    reviewCount++;
    endSwitch = response.switch
    if (response.switch != "true"){
        reviewContinue.style.display = 'none'
    }
})}

reviewContinue.addEventListener('click', function(e) {
    
    if (endSwitch){
        e.preventDefault();
        reviewComment();            
    }
});

function init(){
    while(genre_list.firstChild){
        genre_list.removeChild( genre_list.firstChild );
    }
    while(languageList.firstChild){
        languageList.removeChild( languageList.firstChild );
    }
    while(reviewStars.firstChild){
        reviewStars.removeChild( reviewStars.firstChild );
    }
    while(castDiv.firstChild){
        castDiv.removeChild( castDiv.firstChild );
    }
    while(similar_list.firstChild){
        similar_list.removeChild( similar_list.firstChild );
    }
    while(video.firstChild){
        video.removeChild( video.firstChild );
    }
    while(reviewList.firstChild){
        reviewList.removeChild( reviewList.firstChild );
    }
    if (document.querySelector('#homepage') != null){
        document.querySelector('#homepage').remove();
    }
    //console.log(document.querySelector('#homepage'))
    reviewCount = 1;
    endSwitch = "true";
}
function setttings(id) {
    init();
    $.ajax({
        'url': '/modal',
        'type': 'GET',
        'data': {
            'movie_id': id
        },
        'dataType': 'json'
    }).done(function(response) {
        moviePoster.src = "https://image.tmdb.org/t/p/w342" + response.modal.poster_path
        movieBackground.src = "https://image.tmdb.org/t/p/w1280" + response.modal.backdrop_path;

        modal_title.textContent = response.modal.title
        modal_date.textContent = response.modal.release_date

        mylist.id = id
        review.id = id
        movieId = id
        reviewButton.href = "/review/post/" + id

        if (response.video != "") {
            iframeElement = document.createElement("iframe")
            iframeElement.src = "https://www.youtube.com/embed/" + response.video;
            video.appendChild(iframeElement)
            video.style.marginBottom = "1.5rem"
            video.style.aspectRatio = "2.35 / 1"
        } else {
            video.style.marginBottom = 0
            video.style.aspectRatio = 0
        }

        if (response.modal.homepage != ""){

            let imageLink = document.createElement("img")
            imageLink.src = "/static/images/externalLink.svg"
            
            let homepage = document.createElement("a")
            homepage.setAttribute("id", "homepage")
            homepage.setAttribute("target", "_blank")
            homepage.href = response.modal.homepage
            homepage.setAttribute("class", "flexColContainer")
            homepage.textContent = "公式サイト"

            homepage.prepend(imageLink)
            modalFunction.appendChild(homepage)
        }

        if (response.status == "True") {
            let img = myListButton.querySelector("img")
            img.src = "/static/images/check.svg"
            img.alt = "mylist already added"
            myListSwitch = true
        }
        // review avg num
        if (response.review_rate != 0) {
            modal_review.textContent = response.review_rate;
            modal_review.style.color = "#ffffff";
            modal_review.style.fontSize = "1rem";
        } else {
            modal_review.textContent = "レビューがないので計算できません＞ ＜";
            modal_review.style.color = "#0080de";
            modal_review.style.fontSize = "0.75rem";

            const li = document.createElement("li");
            li.textContent = "最初の投稿者になりませんか?";
            li.style.border = "none";
            reviewList.appendChild(li);
        }
        // あらすじ
        if (response.modal.overview != "") {
            overview.textContent = response.modal.overview;
        } else {
            overviewContainer.style.display = "none";
        }

        for (const language of response.modal.spoken_languages ) {
            var newElement = document.createElement("li");
            newElement.textContent = language.name;
            languageList.appendChild(newElement)
        }

        for (const genre of response.modal.genres) {
            var newElement = document.createElement("li");
            newElement.textContent = genre.name;
            genre_list.appendChild(newElement)
        }
        
        for (const cast of response.casts) {
            var newDiv = document.createElement("div");
            newDiv.setAttribute("class", "castRole");

            var newElement = document.createElement("p");
            var newElement2 = document.createElement("p");

            newElement.textContent = cast.known_for_department;
            newElement2.textContent = cast.character + cast.name;
            newDiv.appendChild(newElement);
            newDiv.appendChild(newElement2);

            castDiv.appendChild(newDiv);
        }
        
        
        for (let i = 0; i < Math.floor(response.review_rate); i++){
            var listItem = document.createElement("li");
            var reviewStar = '<svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_474_926)"><path d="M18 25.905L27.27 31.5L24.81 20.955L33 13.86L22.215 12.945L18 3L13.785 12.945L3 13.86L11.19 20.955L8.73 31.5L18 25.905Z" fill="#FFFD54"/></g><defs><clipPath id="clip0_474_926"><rect width="36" height="36" fill="white"/></clipPath></defs></svg>';

            listItem.innerHTML = reviewStar;
            reviewStars.appendChild(listItem)
        }
        for (const similar of response.similars) {
            console.log(similar)
            if (similar.backdrop_path == null) {
                continue
            }
            var newElement = document.createElement("li");
            newElement.setAttribute("class", "swiper-slide similarMovie"); // add class swiper-slide
            var newElement2 = document.createElement("img");
            newElement2.setAttribute("class", "clickDetail");
            newElement2.setAttribute("id", similar.id);
            newElement2.src = "https://image.tmdb.org/t/p/w300_and_h450_bestv2" + similar.poster_path;
            newElement.appendChild(newElement2);
            similar_list.appendChild(newElement);
            
            newElement2.addEventListener("click", function (e) {
                setttings(this.id);
            });
        }

        // clipboard
        copyButton.addEventListener("click", function (e) {
            // navigator.clipboard.writeText("title") // local環境では不可
            let str = location.host+ "/title/" + movieId
            let listener = function(e){
                e.clipboardData.setData("text/plain" , str);
                e.preventDefault();
                document.removeEventListener("copy", listener);
            }
            document.addEventListener("copy" , listener);
            document.execCommand("copy");
        })

        myListButton.addEventListener("click", function (e) {
            console.log(e.target)
            let img = e.target
            if (myListSwitch == true) {
                img.src = "/static/images/myList.svg"
                img.alt = "mylist add link"
                myListSwitch = false
            } else {
                img.src = "/static/images/check.svg"
                img.alt = "mylist already added"
                myListSwitch = true
            }
        })
    
        reviewComment();
        document.getElementById('easyModal').style.visibility = 'visible';
    }).fail(function () {
        alert('ページの取得に失敗しました。');
    });
}



for (i = 0; i < clickDetail.length; i++) {
    clickDetail[i].addEventListener("click", function (e) {
        setttings(this.id);
    });
}

let titleId = document.querySelector('.titleId')
console.log(titleId)
if (titleId != null){
    setttings(titleId.id);
}