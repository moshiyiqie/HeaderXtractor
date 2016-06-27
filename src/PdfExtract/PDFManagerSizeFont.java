package PdfExtract;

import java.io.IOException;
import java.util.List;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.util.PDFTextStripper;
import org.apache.pdfbox.util.TextPosition;

public class PDFManagerSizeFont {
	public static void main(String args[]) throws IOException{
		PDFManager pdfm = new PDFManager();
		//String path = args[0];
		String path = "C:/ZONE/test3.pdf";
		PDDocument pdd = PDDocument.load(path);
		PDFTextStripper stripper = new PDFTextStripper() {
		    protected void writeString(String text, List<TextPosition> textPositions) throws IOException
		    {
		        StringBuilder builder = new StringBuilder();
		        boolean first = true;
		        for (TextPosition position : textPositions)
		        {
		        	if(first){
		        		first= false;
		        		String baseFont = position.getFont().getBaseFont();
		        		if (baseFont != null){
		        			builder.append('[').append(baseFont).append(']');
		        			builder.append("|||[").append(position.getFontSizeInPt()).append(']');
		        		}
		        	}
		        	builder.append(position.getCharacter());
		        }
		        builder.append(' ');
		        writeString(builder.toString());
		    }
		};
		String text = stripper.getText(pdd);
		System.out.println(text);
	}
}
