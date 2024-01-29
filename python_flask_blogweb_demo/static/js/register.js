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
//
//
//
// // 当需要创建对象存储时，此事件会被触发
// request.onupgradeneeded = function(event) {
//     db = event.target.result;
//     if (!db.objectStoreNames.contains('users')) {
//         var objectStore = db.createObjectStore('users', { keyPath: 'id', autoIncrement: true });
//         objectStore.createIndex('phone', 'phone', { unique: true });
//         objectStore.createIndex('email', 'email', { unique: true });
//         objectStore.createIndex('username', 'username');
//         objectStore.createIndex('job', 'job');
//         objectStore.createIndex('sign', 'sign');
//         objectStore.createIndex('headImg', 'headImg');
//     }
// };

function addUser() {
    var phone = document.getElementById("phone").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var username = document.getElementById("username").value;
    var job = document.getElementById("job").value;
    var code = document.getElementById("smsCode").value;
    check();



    // hashencode
    password = CryptoJS.SHA256(password).toString();

        // 创建JSON对象
    var formData = {
        username: username,
        phone: phone,
        email: email,
        job: job,
        code: code,
        password: password // 注意：实际应用中应该在客户端对密码进行哈希处理
    };

    // 将对象转换为JSON字符串
    var jsonData = JSON.stringify(formData);

    // 发送JSON数据
    fetch('../register', { // 替换成您的服务器端点
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert("注册成功！");
        location.href="login.html";
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("注册失败！");
    });

}


function check(){
    var phone = document.getElementById("phone").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var password2 = document.getElementById("password2").value;

    // 手机号码正则表达式
    var phoneRegex = /^1[3-9]\d{9}$/;
    if (!phoneRegex.test(phone)) {
        alert("请输入有效的手机号码！");
        event.preventDefault(); // 阻止表单提交
    }

    // 电子邮件正则表达式
    var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailRegex.test(email)) {
        alert("请输入有效的电子邮件地址！");
        event.preventDefault(); // 阻止表单提交
    }

    // 密码简单校验（可根据需要调整）
    if (password.length < 6) {
        alert("密码长度至少为6位！");
        event.preventDefault(); // 阻止表单提交
    }
    if(password!=password2){
        alert("密码不一致！");
        event.preventDefault(); // 阻止表单提交
    }
}

function sendSms() {
    var email = document.getElementById("email").value;
    fetch('../email_captcha/?email=' + email, { // 替换成您的服务器端点
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("发送失败！");
    });

    // 开始倒计时
    var seconds = 60; // 倒计时秒数
    var btn = document.getElementById('sendSmsBtn');
    btn.disabled = true; // 禁用按钮

    var interval = setInterval(function() {
        btn.textContent = seconds + "秒后重试";
        seconds--;

        if (seconds <= 0) {
            clearInterval(interval);
            btn.textContent = "发送验证码";
            btn.disabled = false; // 启用按钮
        }
    }, 1000);
}



