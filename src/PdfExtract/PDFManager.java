package PdfExtract;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.util.PDFTextStripper;
import org.apache.pdfbox.util.TextPosition;

public class PDFManager {
	private PDFTextStripper stripper;
	private PDFTextStripper textStripper;
	private ArrayList<ArrayList<TextPosition> > pages;//按页存的textpos序列
	private ArrayList<TextPosition> tmpTxtPosArr = new ArrayList<>();
	private ArrayList<ArrayList<ArrayList<TextPosition>>> txtPosMat=new ArrayList<>();
	
	private double SAMELINE = 8.0;//if two char's y pos diff smaller than this value regarded in same line. With test, 5.0~11.0 is ok
	/**获得第i页的一行行的字符
	 * @param i
	 * @return
	 */
	private ArrayList<ArrayList<TextPosition>> getLinesofIthPage(int i){
		ArrayList<ArrayList<TextPosition>> lines = new ArrayList<>();
		tmpTxtPosArr=new ArrayList<>();
		for(TextPosition tp:pages.get(i)){
			if(tmpTxtPosArr.isEmpty() || Math.abs(tp.getY() - tmpTxtPosArr.get(0).getY()) <= SAMELINE ){
				tmpTxtPosArr.add(tp);
			}else{
				lines.add(tmpTxtPosArr);
				tmpTxtPosArr=new ArrayList<>();
				tmpTxtPosArr.add(tp);
			}
		}
		if(!tmpTxtPosArr.isEmpty()) lines.add(tmpTxtPosArr);
		return lines;
	}
	
	public PDFManager() throws IOException {
		stripper = new PDFTextStripper();
	}
	
	/**给出pdf的路径，将整个pdf的textpos序列输入到txtposArr中
	 * @param path
	 * @throws IOException
	 */
	public void loadPDF(String path) throws IOException{
		PDDocument pdd = PDDocument.load(path);
	    pages= new ArrayList<ArrayList<TextPosition> >();
	    textStripper = new PDFTextStripper(){
	        @Override
	        protected void processTextPosition(TextPosition text) {
	        	tmpTxtPosArr.add(text);
	        }
	    };
	    textStripper.setSuppressDuplicateOverlappingText(false);
	    for(int pageNum = 0;pageNum<pdd.getNumberOfPages();pageNum++){
	        PDPage page = (PDPage) pdd.getDocumentCatalog().getAllPages().get(pageNum);
	        tmpTxtPosArr=new ArrayList<>();
	        textStripper.processStream(page, page.findResources(), page.getContents().getStream());
	        pages.add(tmpTxtPosArr);
	    }
	    pdd.close();
	    
	    //制作txtpos矩阵
	    for(int i=0;i<pages.size();i++){
	    	txtPosMat.add(getLinesofIthPage(i));
	    }
	}
	
	/**获取第i页的pdf文档的plain text
	 * @param i
	 * @return
	 */
	public String getIthPagePlainText(int i){
		StringBuffer sb = new StringBuffer();
		for(ArrayList<TextPosition> tps:txtPosMat.get(i)){
			for(TextPosition tp:tps){
				sb.append(tp.getCharacter());
			}
			sb.append('\n');
		}
		return sb.toString();
	}
	/**获取第i页第j行的pdf文档的plain text
	 * @param i
	 * @return
	 */
	public String getIthPageJthLinePlainText(int i,int j){
		StringBuffer sb = new StringBuffer();
		for(TextPosition tp:txtPosMat.get(i).get(j)){
			sb.append(tp.getCharacter());
		}
		return sb.toString();
	}
	
	/**获取pdf文档的页数
	 * @return
	 */
	public int getPageNum(){
		return pages.size();
	}
	
	public ArrayList<ArrayList<TextPosition> > getPages(){
		return pages;
	}
	
	/**输入pdf路径，获得整个pdf的raw text
	 * @param path
	 * @return
	 * @throws IOException
	 */
	public String getAllText(String path) throws IOException{
		PDDocument doc = PDDocument.load(path);
		return stripper.getText(doc);
	}
	
	public static void main(String args[]) throws IOException{
		PDFManager pdfm = new PDFManager();
		pdfm.loadPDF("C:/ZONE/TaoResearch/pdf_use_style_info.pdf");
		//System.out.println(pdfm.getIthPagePlainText(0));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,0));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,1));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,2));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,3));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,4));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,5));
		System.out.println(pdfm.getIthPageJthLinePlainText(0,6));
	}
}
