// // 打开数据库
// var db;
// var request = window.indexedDB.open("UserDatabase", 1);
//
// request.onerror = function(event) {
//     console.log("数据库打开失败");
// };
//
// request.onsuccess = function(event) {
//     db = request.result;
//     console.log("数据库打开成功");
// };


// 保存用户名
function saveUsername(phone,password) {
    localStorage.setItem("username", phone);
    localStorage.setItem("username", password);
}

// 加载页面时填充用户名
window.onload = function() {
    if (localStorage.getItem("phone")) {
        document.getElementById("phone").value = localStorage.getItem("phone");
    }
};

function validateUserByPhone(phone, inputPassword) {
    var phone = document.getElementById("phone").value;
    var password = document.getElementById("password").value;
    // hashencode
    password = CryptoJS.SHA256(password).toString();

        // 创建JSON对象
    var formData = {
        phone: phone,        password: password
    };

    // 将对象转换为JSON字符串
    var jsonData = JSON.stringify(formData);

    // 发送JSON数据
    fetch('../login', { // 替换成您的服务器端点
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert("登录成功！");

        // 存储jwt
        let jwt = data.access_token; // 请根据实际响应结构调整这一行
        // 存储 JWT 到 localStorage
        localStorage.setItem('jwt', jwt);
        location.href="user.html";
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("登录失败！");
    });
}


// 当表单提交时
function checkUser(){
    //console.log(1);
    var phone = document.getElementById("phone").value;
    var password = document.getElementById("password").value;
    // 如果用户选择记住账号
    if (document.getElementById("rememberMe").checked) {
        saveUsername(phone,password);
    }
    validateUserByPhone(phone,password);


}
