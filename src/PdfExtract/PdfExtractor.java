package PdfExtract;

import org.w3c.dom.Document;

import java.awt.geom.Rectangle2D;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.pdfbox.*;
import org.apache.pdfbox.cos.COSDocument;
import org.apache.pdfbox.pdfparser.PDFParser;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotation;
import org.apache.pdfbox.util.PDFTextStripper;
import org.apache.pdfbox.util.PDFTextStripperByArea;
import org.apache.pdfbox.util.TextPosition;
public class PdfExtractor {
	public static void main(String args[]) throws IOException{
		//Document luceneDocument = LucenePDFDocument.getDocument( ... );
	    PDDocument pdd = PDDocument.load("C:/ZONE/TaoResearch/pdf_use_style_info.pdf");
	    final StringBuffer extractedText = new StringBuffer();
	    ArrayList<Integer> xbox= new ArrayList<Integer>();
	    PDFTextStripper textStripper = new PDFTextStripper(){
	        @Override
	        protected void processTextPosition(TextPosition text) {
	            extractedText.append(text.getCharacter());
	            System.out.println(text.getCharacter());
	            System.out.println(text.getX());
	            System.out.println(text.getY());
	            if(text.getFontSize()!=1.0 && text.getFontSize()!=9.0)
	            	System.out.println(text.getFontSize());
	            //System.out.println("text position: "+text.toString());
	        }
	    };
	    textStripper.setSuppressDuplicateOverlappingText(false);
	    for(int pageNum = 0;pageNum<pdd.getNumberOfPages();pageNum++){
	        PDPage page = (PDPage) pdd.getDocumentCatalog().getAllPages().get(pageNum);
	        textStripper.processStream(page, page.findResources(), page.getContents().getStream());
	    }
	    pdd.close();
	}
}
