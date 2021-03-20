/**
 * Unit testing the SaintsXCTF Auth api (auth.saintsxctf.com) with Jest.
 * @author Andrew Jarombek
 * @since 7/17/2020
 */

const axios = require('axios');

const instance = axios.create({
    baseURL: process.env.TEST_ENV === 'prod' ? 'https://auth.saintsxctf.com' : 'https://dev.auth.saintsxctf.com',
    timeout: 5000
});

const jwtPattern = /^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$/;

describe('token api', () => {

    it('returns an empty string by default', () => {
        return instance
            .post('/token', {})
            .then((res) => {
                console.info(res.data);
                expect(res.data.result).toEqual("");
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });

    it('returns a jwt when valid credentials are provided', () => {
        return instance
            .post('/token', {
                clientId: 'andy',
                clientSecret: process.env.CLIENT_SECRET
            })
            .then((res) => {
                console.info(res.data);
                expect(res.data.result).toMatch(jwtPattern);
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });

    it('the jwt is well structured', () => {
        return instance
            .post('/token', {
                clientId: 'andy',
                clientSecret: process.env.CLIENT_SECRET
            })
            .then((res) => {
                const [header, payload, _] = res.data.result.split('.');

                const headerBuffer = new Buffer(header, 'base64');
                const headerObject = JSON.parse(headerBuffer.toString('utf-8'));

                expect(headerObject['typ']).toEqual('JWT');
                expect(headerObject['alg']).toEqual('RS256');
                expect(Object.keys(headerObject)).toEqual(['typ', 'alg']);

                const payloadBuffer = new Buffer(payload, 'base64');
                const payloadObject = JSON.parse(payloadBuffer.toString('utf-8'));

                expect(Object.keys(payloadObject)).toEqual(['iat', 'exp', 'iss', 'sub', 'email', 'name']);

                expect(typeof payloadObject['iat']).toEqual('number');
                expect(typeof payloadObject['exp']).toEqual('number');
                expect(typeof payloadObject['iss']).toEqual('string');
                expect(typeof payloadObject['sub']).toEqual('string');
                expect(typeof payloadObject['email']).toEqual('string');
                expect(typeof payloadObject['name']).toEqual('string');

                expect(payloadObject['iss']).toEqual('auth.saintsxctf.com');
                expect(payloadObject['sub']).toEqual('andy');
                expect(payloadObject['email']).toEqual('andrew@jarombek.com');
                expect(payloadObject['name']).toEqual('Andy Jarombek');
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });
});

describe('authenticate api', () => {

    it('returns an empty string by default', () => {
        return instance
            .post('/authenticate', {})
            .then((res) => {
                console.info(res.data);
                expect(res.data.result).toEqual(false);
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });

    it('returns false if the jwt is invalid', () => {
        return instance
            .post('/authenticate', {
                token: 'a.b.c'
            })
            .then((res) => {
                console.info(res.data);
                expect(res.data.result).toEqual(false);
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });

    it('returns true if the jwt is valid', () => {
        return instance
            .post('/token', {
                clientId: 'andy',
                clientSecret: process.env.CLIENT_SECRET
            })
            .then((res) => {
                return instance.post(
                    '/authenticate',
                    {
                        token: res.data.result
                    })
            })
            .then((res) => {
                console.info(res.data);
                expect(res.data.result).toEqual(true);
            })
            .catch((err) => {
                console.error(err);

                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });
});