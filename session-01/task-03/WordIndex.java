import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class WordIndex {

	public static final int LINES_PER_PAGE = 45;
	public static final int MAX_SIZE_LINE = 80;
	public static final int STOP_FREQUENCY_LIMIT = 100;

	public static String[] parseLine(String line) {
		return line.split("\\W+");

	}

	/**
	 * # Global "constants"
	 * 
	 * # Defining a main method makes testing easier class WordIndexData:
	 * 
	 * def __init__(self, word): self.word = word self.frequency = 0 self.pages =
	 * set()
	 * 
	 * def appear_on(self, page): """ Increment frequency of occurrences and store
	 * page without duplicates""" self.frequency += 1 self.pages.add(page)
	 * 
	 * 
	 * 
	 * def main(file_path): stop_words = [] word_index = []
	 * 
	 * 
	 * 
	 * @param args
	 * @throws FileNotFoundException
	 */
	public static void main(String[] args) throws FileNotFoundException {
		int currentPage = 0;
		int lineNumber = 0;
		Set<String> stopWords = new HashSet<String>();
		Map<String, AtomicInteger> frequencies = new HashMap<String, AtomicInteger>();
		Map<String, Set<Integer>> pages = new HashMap<String, Set<Integer>>();

		try (Scanner scanner = new Scanner(new File(args[0]))) {
			while (scanner.hasNextLine()) {
				if (lineNumber % LINES_PER_PAGE == 0) {
					currentPage += 1;
				}

				for (String word : parseLine(scanner.nextLine())) {

					if (stopWords.contains(word)) {
						continue;
					}

					if (!frequencies.containsKey(word)) {
						frequencies.put(word, new AtomicInteger(0));
					}
					frequencies.get(word).incrementAndGet();

					if (!pages.containsKey(word)) {
						pages.put(word, new HashSet<Integer>());
					}
					pages.get(word).add(currentPage);

					if (frequencies.get(word).get() > STOP_FREQUENCY_LIMIT) {
						frequencies.remove(word);
						pages.remove(word);
						stopWords.add(word);
					}
				}
			}
		}

		List<String> sortedWords = new ArrayList<String>(pages.keySet());
		Collections.sort(sortedWords);
		
		for(String word : sortedWords ) {
			List<Integer> sortedPages = new ArrayList<Integer>(pages.get(word));
			Collections.sort(sortedPages);
			System.out.println(String.format("%s - %s", word, sortedPages.toString().replace("[", "").replace("]", "")));
		}
	}
}