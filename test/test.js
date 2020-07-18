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

describe('token api', () => {

    it('returns 401 by default', () => {
        instance
            .get('/token')
            .then((res) => {
                console.info(res);
            })
            .catch((err) => {
                console.info(err);
            });
    });

});