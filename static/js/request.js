function request(url, body, callback) {
    let formRequest = new Request(url, {
        method: 'post',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
        },
        body: body
    })
    fetch(formRequest).then(response => {
        let result = response.json()
        result.then(res => {
            callback(res)
        })
    })
}