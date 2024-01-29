let jwt = localStorage.getItem('jwt');
var content = '# 在这里写下一篇帖子 ##';
var config = {
    // 这里的尺寸必须在这里设置. 设置样式会被 editormd 自动覆盖掉.
    width: "100%",
    // 高度 100% 意思是和父元素一样高. 要在父元素的基础上去掉标题编辑区的高度
    height: "100vh",
    // 编辑器中的初始内容
    markdown: content,
    // 指定 editor.md 依赖的插件路径
    path: "node_modules/editor.md/lib/",
    saveHTMLToTextarea : true
};
var testEditor = editormd("editor", config);

function sendContent(){
    var content = testEditor.getHTML();
    console.log(content);
    var title = document.getElementById("title").value;
    var image_path;var video_path;
    // 创建JSON对象
    var formData = new FormData();
     // 提取 URL 中的 post_id
    var urlParams = new URLSearchParams(window.location.search);
    var post_id = urlParams.get('id');

    formData.append("post_id",post_id);
    formData.append("title",title);
    formData.append("content",title);

    // 获取选择的图片文件
    var image_s = document.getElementById('image_s').files[0];
    if (image_s) {
        formData.append('image_s', image_s);
    }
    // 获取选择的视频文件
    var video_s = document.getElementById('video_s').files[0];
    if (video_s) {
        formData.append('video_s', video_s);
    }

    fetch('../postedQuestion_edit',{
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + jwt
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert("添加成功！");
        location.href="list.html";
        // 处理响应数据
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error);
    });
}