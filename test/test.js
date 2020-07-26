/**
 * Unit testing the SaintsXCTF Auth api (auth.saintsxctf.com) with Jest.
 * @author Andrew Jarombek
 * @since 7/17/2020
 */

import axios from 'axios';

const instance = axios.create({
    baseURL: process.env.TEST_ENV === 'prod' ? 'https://auth.saintsxctf.com' : 'https://dev.auth.saintsxctf.com',
    timeout: 1000
});

describe('authenticate api', () => {

    it('returns 403 by default', () => {
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

    it('returns 403 by default', () => {
        instance
            .post('/token')
            .then((res) => {
                expect(true).toBe(false);
            })
            .catch((err) => {
                console.info(err);
                expect(err.message).toEqual("Forbidden");
            });
    });
});