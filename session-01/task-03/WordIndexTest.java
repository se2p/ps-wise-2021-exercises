import static org.junit.Assert.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

public class WordIndexTest {

	private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
	private final ByteArrayOutputStream errContent = new ByteArrayOutputStream();
	private final PrintStream originalOut = System.out;
	private final PrintStream originalErr = System.err;

	@Rule
	public TemporaryFolder temp = new TemporaryFolder();

	@Before
	public void setUpStreams() {
		System.setOut(new PrintStream(outContent));
		System.setErr(new PrintStream(errContent));
	}

	@After
	public void restoreStreams() {
		System.setOut(originalOut);
		System.setErr(originalErr);
	}

	@Test
	public void testWithEmptyFile() throws IOException {
		File emptyFile = temp.newFile();
		WordIndex.main(new String[] { emptyFile.getAbsolutePath() });
		assertEquals("", outContent.toString());
	}

	@Test
	public void testWithOneLineFile() throws IOException {
		File oneLineFile = temp.newFile();
		try(PrintStream printFile = new PrintStream( oneLineFile )){
			printFile.println("blabla");
		}
		WordIndex.main(new String[] { oneLineFile.getAbsolutePath() });
		assertEquals("blabla - 1\n", outContent.toString());
	}

    // TODO Create a 3rd file
}