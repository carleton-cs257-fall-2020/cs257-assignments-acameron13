// Alison Cameron and Adam Nik

function navigateAndSearch(noc){
    console.log("called correctly");
    console.log(noc);
    searchByNoc = noc;
    console.log("searchByNoc: ", searchByNoc);
    window.location.href = 'search.html';
}

function getSearchByNoc(){
    return searchByNoc;
}
