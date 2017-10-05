// To manage marking sheets in Google Sheets

/*
 * Adds menu buttons
 */
function onOpen() {
   var ss = SpreadsheetApp.getActiveSpreadsheet();
   var menuEntries = [];
   menuEntries.push({name: "Generate student sheets", functionName: "cloneSampleSheet"});
   menuEntries.push({name: 'Save All Sheets as PDFs', functionName: 'saveSheetsAsPDF'});
   menuEntries.push(null); // line separator
   menuEntries.push({name: 'Delete all student sheets', functionName: 'deleteSheets'});
   ss.addMenu("Scripts", menuEntries);
};

function deleteSheets() {
  var confirm = Browser.msgBox('CAUTION','Are you sure you want to delete student sheets ?', Browser.Buttons.OK_CANCEL);
  if(confirm=='ok') {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheetsCount = ss.getNumSheets();
    var sheets = ss.getSheets();

    for (var i = 0; i < sheetsCount; i++){
      var sheet = sheets[i];

      // Don't delete if sheet is hidden
      if (sheet.isSheetHidden()) {
        continue;
      }

      var sheetName = sheet.getName();
      Logger.log(sheetName);
      if (sheetName != 'sample' && sheetName != 'ids') {
        Logger.log("DELETE!");
        ss.deleteSheet(sheet);
      }
    }
  }
}

/*
Copies 'sample' sheet n times, where n is the number of students found in
the 'ids' sheet. The sheet will be named with these
*/
function cloneSampleSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // Get ids
  var sheet = ss.getSheetByName('ids');
  var ids = sheet.getRange("A1:A").getValues();
  var ids = ids.filter(String);
  var ids_c = ids.length;

  // Copy sheets
  for (var i in ids) {

    id_name = ids[i][0];
    id_only = id_name.split("-")[0]
    var old = ss.getSheetByName(id_name);
    if (old) {
      //ss.deleteSheet(old); // or old.setName(new Name);
      // If sheet exists, don't create
      continue;
    }
    // Clone sheet to generic name
    var sheet = ss.getSheetByName('sample').copyTo(ss);

    SpreadsheetApp.flush(); // Utilities.sleep(2000);
    sheet.setName(id_name);
    var range = sheet.getRange(4,2);
    range.setValue(id_only);
  }
  // Sort the sheets
  sortGoogleSheets();
}

function saveSheetsAsPDF() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var url = ss.getUrl().replace(/edit$/,'');
  var parents = DriveApp.getFileById(ss.getId()).getParents();
  if (parents.hasNext()) {var folder = parents.next();}
  else {folder = DriveApp.getRootFolder();}
  var sheets = ss.getSheets();
  for (var i=0; i<sheets.length; i++) {
    if (ss.getName() == 'sample' || ss.getName() == 'ids') {continue;}
    var url_ext = 'export?exportFormat=pdf&format=pdf&gid=' + sheets[i].getSheetId()
    +'&size=letter&portrait=true&fitw=true&sheetnames=false'
    +'&printtitle=false&pagenumbers=false&gridlines=false&fzr=false';
    var options = {headers:{'Authorization':'Bearer '+ScriptApp.getOAuthToken()}}
    var response = UrlFetchApp.fetch(url + url_ext, options);
    var filename = ss.getName()+' - '+sheets[i].getName()+'.pdf'
    var files   = folder.getFilesByName(filename);
    if(!files.hasNext()){
       Logger.log("file "+filename+" will be created");
    }
    else{
       // files is an iterator
      while (files.hasNext()) {
        file = files.next();
        file.setTrashed(true);
      }
       Logger.log("file "+filename+" has been deleted");
    }
    var blob = response.getBlob().setName(filename);
    folder.createFile(blob);
  }
}


/* Credit: https://gist.github.com/chipoglesby/26fa70a35f0b420ffc23 */
function sortGoogleSheets() {

  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // Store all the worksheets in this array
  var sheetNameArray = [];
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    sheetNameArray.push(sheets[i].getName());
  }

  sheetNameArray.sort();

  // Reorder the sheets.
  for( var j = 0; j < sheets.length; j++ ) {
    ss.setActiveSheet(ss.getSheetByName(sheetNameArray[j]));
    ss.moveActiveSheet(j + 1);
  }
  var sheet = ss.getSheets()[0];
  SpreadsheetApp.setActiveSheet(sheet);
}
