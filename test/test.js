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
                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });
});