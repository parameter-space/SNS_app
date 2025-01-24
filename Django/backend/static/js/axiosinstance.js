const accessToken = getCookie("access");

let headers = { 
    'X-CSRFToken': getCookie("csrftoken"),
}

if (accessToken) { // access token 값이 있을 경우엔 그것도 헤더에 담기위해 실행
    headers['Authorization'] = `Bearer ${accessToken}`; 
}
const axiosInstance = axios.create({ // axios instance 생성
    baseURL: '/',
    headers: headers,
});