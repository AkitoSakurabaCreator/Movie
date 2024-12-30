


var positionY;					/* スクロール位置のY座標 */
var STORAGE_KEY = "scrollY";	/* ローカルストレージキー */

/*
 * checkOffset関数: 現在のスクロール量をチェックしてストレージに保存
 */
function checkOffset(){
	positionY = window.pageYOffset;
	localStorage.setItem(STORAGE_KEY, positionY);
}

/*
 * 起動時の処理
 *
 *		ローカルストレージをチェックして前回のスクロール位置に戻す
 */
window.addEventListener("load", function(){
	// ストレージチェック
	positionY = localStorage.getItem(STORAGE_KEY);

	// 前回の保存データがあればスクロールする
	if(positionY !== null){
		scrollTo(0, positionY);
	}

	// スクロール時のイベント設定
	window.addEventListener("scroll", checkOffset, false);
});