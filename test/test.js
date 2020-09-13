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

describe('authenticate api', () => {

    it.skip('returns 403 by default', () => {
        expect.assertions(1);
        instance
            .post('/authenticate')
            .then((res) => {
                expect(true).toBe(false);
            })
            .catch((err) => {
                console.info(err);
                expect(err.message).toEqual("Forbidden");
            });
    });
});

describe('token api', () => {

    it.skip('returns 500 by default', () => {
        return instance
            .post('/token')
            .then(() => {
                // 'then' block should not be called.
                expect(true).toBe(false);
            })
            .catch((err) => {
                console.info(err);
                expect(err.message).toEqual("Missing Authentication Token");
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

                const result = JSON.parse(res.data).result;
                expect(result).toMatch(jwtPattern);
            })
            .catch((err) => {
                // 'catch' block should not be called.
                expect(true).toBe(false);
            });
    });
});