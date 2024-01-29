let jwt = localStorage.getItem('jwt');

document.addEventListener('DOMContentLoaded', function() {
    fetch('../userinfo',{
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + jwt
        }
    }) // 替换为后端提供用户信息的实际路由
        .then(response => response.json())
        .then(data => {
            // 假设返回的数据对象中包含 username, job, sign, headImg 字段
            document.getElementById('username').textContent = data.username;
            document.getElementById('job').textContent = data.job;
            document.querySelector('.签名档').textContent = data.sign;
            document.querySelector('.头像 img').src = data.headImg;
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
});

