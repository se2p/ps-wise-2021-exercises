const { worker } = require('cluster');
const fs = require('fs')

const LINES_PER_PAGE = 45
const STOP_FREQUENCY_LIMIT = 100


var main = function(inputFile) {
    var array = fs.readFileSync(inputFile).toString().split("\n");
    var currentPage = 0 
    var stopWords = []
    var wordIndex = []

    for(lineNumber in array) {
        
        if(lineNumber % LINES_PER_PAGE == 0){
            currentPage += 1
        }

        for(let word of array[lineNumber].split(/\W+/)){
            if(word.length == 0 ){
                // Skip empty words
                continue;
            }
            
            // Make sure we normalize
            word = word.toLowerCase()
            
            if( word in stopWords ){
                // Skip stop words. Q: can we make the empty word a stop word?
                continue;
            }

            x = wordIndex.find( x => x['word'] == word )
            if( x ){
                // Word is there
                x['freq'] += 1
                // Avoid duplicates
                if (! currentPage in x['pages']){
                   x['pages'].push(currentPage)
                }

                if( x['freq'] > STOP_FREQUENCY_LIMIT){
                    const index = wordIndex.indexOf(x);
                    wordIndex.splice(index, 1);
                    stopWords.push(word)
                }
            } else {
                var x = {"word" : word, "freq" : 1, "pages" : [currentPage] }
                // Q: can you implement an insert operation that place x in a way to have elements sorted by word?
                wordIndex.push(x)
            }
        }            
    }

    // Sort
    wordIndex.sort((a, b) => (a.word > b.word) ? 1 : -1)

    // Pring
    wordIndex.forEach(x => console.log(x["word"]+" - "+x["pages"].join(", ")))

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