function getCookie(name) { // name에 쿠키 이름이 담김
    var cookieName = name + "="; 
    var decodedCookie = decodeURIComponent(document.cookie); 
    var cookieArray = decodedCookie.split(';');
    
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i];
        while (cookie.charAt(0) == ' ') { 
            cookie = cookie.substring(1); 
        }
        
        if (cookie.indexOf(cookieName) == 0) {
            return cookie.substring(cookieName.length, cookie.length); 
        }
    }
    
    return ""; 
}

/*
동작 예시
document.cookie = "username=John Doe; age=30"; 이렇게 쿠키가 하나의 문자열로 통째로 넘어올 때
**위의 경우에 ; 기준으로 split 해도 공백 문자열이 다음 배열에 저장될 수 있음 " age=30"이렇게

console.log(getCookie("username")); // "John Doe"
console.log(getCookie("age")); // "30"
console.log(getCookie("gender")); // ""
이렇게 되는 것
*/