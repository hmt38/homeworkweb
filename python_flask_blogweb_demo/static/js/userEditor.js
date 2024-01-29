let jwt = localStorage.getItem('jwt');

function EditUser() {
    // 创建 FormData 对象来构建要提交的表单数据
    var formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('job', document.getElementById('job').value);
    formData.append('sign', document.getElementById('text').value);

    // 获取选择的图片文件
    var headImgFile = document.getElementById('headImg').files[0];
    if (headImgFile) {
        formData.append('headImg', headImgFile);
    }

    // 发送请求到服务器端点
    fetch('../userInfoEditor', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + jwt
        },
        body: formData
        // 不设置 'Content-Type' 头部，浏览器会自动设置
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert("修改成功！");
        location.href="user.html";
        // 处理响应数据
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error);
    });
}
