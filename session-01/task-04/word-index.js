const fs = require('fs')

const LINES_PER_PAGE = 45
const STOP_FREQUENCY_LIMIT = 100

var main = function(inputFile) {
}
  
if (require.main === module) {
    // Pass the arguments to the function
    // argv[0] -> node
    // argv[1] -> this script
    // argv[2] -> the first real input
    main(process.argv[2]);
}
  
/*
Export the main function so it can be called from the tests. This let us testing the
app without creating a subprocess but YOU need to take care of cleaning up and
initializing the app.
*/
module.exports.main = main