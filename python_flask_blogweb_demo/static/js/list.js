
document.addEventListener('DOMContentLoaded', function() {
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        var postList = document.getElementById('postNewList');
        posts.forEach(post => {
            var postItem = `
<!--               </div>-->
<!--               <li>-->
                <div class="板块信息">
                    <h3 class="板块名称">${post.title}</h3>
                    <p class="板块说明">${post.content}<br>
                    ${post.image_path ? `<img src="${post.image_path}" alt="Image" style="max-width: 20%; height: auto;">` : ''}<br>
                    ${post.video_path ? `<video src="${post.video_path}" controls style="max-width: 50%; height: auto;"></video>` : ''}
                    <!-- 其他信息 -->
                    </p>

                    <div class="查看详情">
                        <a href="postedEditor.html?id=${post.id}">编辑>></a>
                    </div>

                    <div class="点击">
                        <div class="数量">
                            <div>点击次数</div>
                            <div>100</div>
                        </div>
                        <div>
                            <div>主题数</div>
                            <div>10</div>
                        </div>
                    </div>
                
<!--               </li>-->

            `;
            postList.innerHTML += postItem;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
