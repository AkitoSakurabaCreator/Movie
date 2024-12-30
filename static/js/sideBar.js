    const container = document.querySelector('.container')
    const sidebar = document.querySelector('.sidebar')
    let sidebarSw = true
    var ua = navigator.userAgent
    function smart(){
        container.style.paddingLeft = '0px'
        document.querySelector('.sidebarMenu').addEventListener('click', function(e) {
            if (sidebarSw){
                sidebar.style.visibility = 'hidden'
            }else{
                sidebar.style.visibility = 'visible'
            }
            sidebarSw = !sidebarSw
        });
    }
    if(ua.indexOf('iPhone') > 0){
        smart();
    }else if(ua.indexOf("Android") > 0 && ua.indexOf("Mobile") > 0){
        smart();
    }else if(ua.indexOf("iPad") > 0){
        smart();
    }else if(ua.indexOf("iPod") > 0){
        smart();
    }else{
        sidebar.style.visibility = 'visible'
        document.querySelector('.sidebarMenu').addEventListener('click', function(e) {
            if (sidebarSw){
                container.style.paddingLeft = '0px'
                sidebar.style.visibility = 'hidden'
            }else{
                container.style.paddingLeft = '256px'
                sidebar.style.visibility = 'visible'
            }
            sidebarSw = !sidebarSw
            
        });
    }
