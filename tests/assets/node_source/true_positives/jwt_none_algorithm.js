const jose = require("jose");
const { JWK, JWT } = jose;
const token = JWT.verify('token-here', JWK.None);

function verifyJwt() {
    let jwt = require("jsonwebtoken");
    let secret = 'some-secret';
    jwt.verify('token-here', secret, { algorithms: ['RS256', 'none'] }, function (err, payload) {
        console.log(payload);
    });
}

