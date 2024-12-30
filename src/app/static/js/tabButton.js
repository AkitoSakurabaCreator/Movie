const tabButtons = document.querySelectorAll('.tabButton');
    for(const tab of tabButtons) {
        tab.addEventListener("click", (e) => {
            // すべてのタブのseletedを削除
            for(const tabButton of tabButtons) {
                tabButton.classList.remove("tabSelected");
            }
            // クリックされたタブにtabSelectedを追加
            e.target.classList.add("tabSelected");

            const tabContents = document.querySelectorAll(".tabContent");
            // すべての.tabContentから.tabActiveを削除
            for(const tabContent of tabContents) {
                tabContent.classList.remove("tabActive");
            }

            // クリックされた.tabButtonのidから、.tabContentのidを取得
            const activeTabContentId = (e.target.getAttribute("id") === "detail") ? "detailTab" : "reviewTab";
            // .tabContentのidから表示する.tabContentに.tabActiveを追加
            const activeTabContent = document.getElementById(activeTabContentId);
            activeTabContent.classList.add("tabActive");
        })
    }