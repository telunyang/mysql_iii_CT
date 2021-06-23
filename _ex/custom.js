//選擇放置查詢結果的 div 元素
const div_result = document.querySelector("div#results");

//選擇取得所有 youtube 列表的 button 按鈕元素
const btn_query = document.querySelector("button#query");

//註冊「取得 youtube 列表」的按鈕 click 事件
btn_query.addEventListener("click", function(event){
    //取得所有 youtube 列表
    fetch("/youtube",{
        method: "GET"
    }).then(function(response){
        return response.text();
    }).then(function(json){
        //將 json 轉成物件
        const dictData = JSON.parse(json);
        
        //若是回傳結果為 True，則將 results 屬性的內容呈現在網路上
        if(dictData["success"]){
            let html = ``;
            for(let result of dictData["results"]){
                html += `<div class="col" data-id="${result['id']}">
                <div class="card shadow-sm">
                <img class="bd-placeholder-img card-img-top" src="${result['img']}">
                <div class="card-body">
                <p class="card-text">
                <input type="text" class="form-control update" value="${result['title']}" data-id="${result['id']}">
                </p>
                <div class="d-flex justify-content-between align-items-center">
                <div class="btn-group">
                <a class="btn btn-sm btn-outline-secondary" href="${result['link']}" target="_blank">觀看影片</a>
                <a class="btn btn-sm btn-outline-secondary delete" href="#" data-id="${result['id']}">刪除影片</a>
                </div>
                <small class="text-muted">?? mins</small>
                </div>
                </div>
                </div>
                </div>`;
            }

            //呈現查詢結果
            div_result.innerHTML = html;
        } else {
            alert(dictData["info"]);
        }
    });
});

//選擇輸入影音標題的 input 元素
const input_title = document.querySelector("input#title");

//選擇搜尋按鈕 button 的元素
const btn_search = document.querySelector("button#search");

//註冊搜尋按鈕的 click 事件
btn_search.addEventListener("click", function(event){
    //取得搜尋文字
    let title_value = input_title.value;

    //進行檢索
    fetch("/youtube/title", {
        method: "POST",
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({ title: title_value })
    }).then(function(response){
        return response.text();
    }).then(function(json){
        //將 json 轉成物件
        const dictData = JSON.parse(json);
        
        //若是回傳結果為 True，則將 results 屬性的內容呈現在網路上
        if(dictData["success"]){
            let html = ``;
            for(let result of dictData["results"]){
                html += `<div class="col" data-id="${result['id']}">
                <div class="card shadow-sm">
                <img class="bd-placeholder-img card-img-top" src="${result['img']}">
                <div class="card-body">
                <p class="card-text">
                <input type="text" class="form-control update" value="${result['title']}" data-id="${result['id']}">
                </p>
                <div class="d-flex justify-content-between align-items-center">
                <div class="btn-group">
                <a class="btn btn-sm btn-outline-secondary" href="${result['link']}" target="_blank">觀看影片</a>
                <a class="btn btn-sm btn-outline-secondary delete" href="#" data-id="${result['id']}">刪除影片</a>
                </div>
                <small class="text-muted">?? mins</small>
                </div>
                </div>
                </div>
                </div>`;
            }

            //呈現查詢結果
            div_result.innerHTML = html;
        } else {
            alert(dictData["info"]);
        }
    });
});


//註冊所有使用到「點擊」事件的元素
document.addEventListener("click", function(event){
    if(event.target){
        if( event.target.tagName.toLowerCase() == 'a' && event.target.classList.contains('delete') ){
            //預防預設事件觸發，方便之後撰寫自訂事件觸發的程式碼
            event.preventDefault();

            //取得點擊時的 a 元素
            const a = event.target;

            //取得 a 元素的屬性值 (id)
            let id = a.getAttribute('data-id');

            //刪除指定 id 的資料
            fetch(`/youtube/${id}`,{
                method: "DELETE"
            }).then(function(response){
                return response.text();
            }).then(function(json){
                //將 json 轉成物件
                const dictData = JSON.parse(json);
                
                //若是回傳結果為 True，則將 results 屬性的內容呈現在網路上
                if(dictData["success"]){
                    alert(dictData["info"]);

                    //將點選的元素刪除
                    document.querySelector(`div.col[data-id="${id}"]`).remove();
                } else {
                    alert(dictData["info"]);
                }
            });
        }
    }
});

//註冊所有使用到「離開焦點」事件的元素
document.addEventListener("focusout", function(event){
    if(event.target){
        if( event.target.tagName.toLowerCase() == 'input' && event.target.classList.contains('update') ){
            //預防預設事件觸發，方便之後撰寫自訂事件觸發的程式碼
            event.preventDefault();
            
            //取得離開焦點時的 input 元素
            const input = event.target;

            //取得 input 元素的屬性值
            let id = input.getAttribute('data-id');
            let title_value = input.value;

            //更新指定 id 的資料
            fetch(`/youtube/${id}`,{
                method: "POST",
                headers: {'content-type': 'application/json'},
                body: JSON.stringify({ title: title_value })
            }).then(function(response){
                return response.text();
            }).then(function(json){
                //將 json 轉成物件
                const dictData = JSON.parse(json);
                
                //若是回傳結果為 True，則將 results 屬性的內容呈現在網路上
                if(dictData["success"]){
                    alert(dictData["info"]);
                } else {
                    alert(dictData["info"]);
                }
            });
        }
    }
});