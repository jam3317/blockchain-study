// provider.send(payload, callback) 형태의 함수를 await로 쓸 수 있게 바꿔 준다.
// (강의 사이트에는 숨겨진 파일이라 같은 역할로 직접 만들었다.)
module.exports = function promisify(fn) {
    return function (payload) {
        return new Promise((resolve, reject) => {
            fn.call(this, payload, (err, response) => (err ? reject(err) : resolve(response)));
        });
    };
};
