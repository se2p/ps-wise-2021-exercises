clean:
	rm *.class
	

WordIndex.class : WordIndex.java
	javac WordIndex.java

WordIndexTest.class : WordIndexTest.java WordIndex.class
	javac -cp .:hamcrest-2.2.jar:junit-4.12.jar WordIndexTest.java

run : WordIndex.class
	java WordIndex ../test-data/one-line.txt   

run-empty : WordIndex.class
	java WordIndex ../test-data/empty.txt

test : WordIndexTest.class WordIndex.class
	java -cp .:hamcrest-2.2.jar:junit-4.12.jar org.junit.runner.JUnitCore WordIndexTest

