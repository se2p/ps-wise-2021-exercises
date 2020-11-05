// Maybe use .strict
const assert = require('assert');

describe('Basic Tests', function() {
    
    describe('Runs correct version of node.', function(){
        it('Version of node must be v10.23.0', function() {
            assert.equal(process.version, 'v10.23.0');
        });
    });
});