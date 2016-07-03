package PdfExtract;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.util.PDFTextStripper;
import org.apache.pdfbox.util.TextPosition;

public class PDFManagerSizeFont {
	public static void main(String args[]) throws IOException{
		PDFManager pdfm = new PDFManager();
		//String path = args[0];
		String path = "C:/ZONE/ceshiPDF2/P15-1033.pdf";
		//String path = "/home/hadoop/利用SVM进行头部抽取第一阶段报告.pdf";
		
		//String outputPath = args[1];
		String outputPath = "D:/output.txt";
		
		PDDocument pdd = PDDocument.load(path);
		PDFTextStripper stripper = new PDFTextStripper() {
			int lineNum=0;
		    protected void writeString(String text, List<TextPosition> textPositions) throws IOException
		    {
		    	StringBuilder builder = new StringBuilder();
		    	StringBuilder sizeInfo = new StringBuilder();
		    	lineNum++;
		    	if(lineNum > 600){
		    		writeString(builder.toString());
	        		return;
	        	}
		        boolean first = true;
		        double rightPos = 0.0;
		        for (TextPosition position : textPositions)
		        {
		        	if(first){
		        		first= false;
		        		String baseFont = position.getFont().getBaseFont();
		        		if (baseFont != null){
		        			builder.append('[').append(baseFont).append(']');
		        			builder.append("|||").append(position.getFontSizeInPt()).append("");
		        			builder.append("|||").append(position.getY());
		        			builder.append("|||").append(position.getX()).append("|||");
		        		}
		        	}
		        	builder.append(position.getCharacter());
		        	sizeInfo.append(position.getFontSizeInPt()).append(",");
		        	rightPos = position.getX() + position.getWidth();
		        }
		        builder.append("|||"+ rightPos + "|||").append(sizeInfo).append(" ");
		        writeString(builder.toString());
		    }
		};
		String text = stripper.getText(pdd);
		PrintWriter pw = new PrintWriter(new FileWriter(outputPath));
		pw.println(text);
		pw.close();
		//System.out.println(text);
	}
}
