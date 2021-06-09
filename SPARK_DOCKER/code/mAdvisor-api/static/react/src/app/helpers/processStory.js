//function to get first card details of provided node slug
export function getFirstCard(output, node_slug) {
  var node = fetchNodeFromTree(node_slug, output);
  if (node.listOfCards.length > 0) {
    return node.listOfCards[0];
  } else {
    if (node.listOfNodes[0].listOfCards.length > 0) {
      return node.listOfNodes[0].listOfCards[0];
    }
  }
}

function fetchCardFromNode(card_slug, node) {
  var listOfCards = node.listOfCards;
  for (var i = 0; i < listOfCards.length; i++) {
    if (listOfCards[i].slug === card_slug) {
      return listOfCards[i];
    }
  }
}


export function fetchNodeFromTree(node_slug, output) {
  var element = output;
  var result = searchTree(element, node_slug);
  return result;
}

function searchTree(element, matchingNode) {
  if (element.slug == matchingNode) {
    return element;
  } else if (element.listOfNodes != null) {
    var i;
    var result = null;
    for (i = 0; result == null && i < element.listOfNodes.length; i++) {
      result = searchTree(element.listOfNodes[i], matchingNode);
    }
    return result;
  }
  return null;
}

export function fetchCard(params, output) {
  var node = null;
  var card = null;
  if (Object.keys(params).length == 3) {
    node = fetchNodeFromTree(params.l1, output);
    card = fetchCardFromNode(params.l2, node);
  } else {
    if (params.l3 != "$") {
      node = fetchNodeFromTree(params.l2, output);
      card = fetchCardFromNode(params.l3, node);
    } else {
      node = fetchNodeFromTree(params.l2, output);
      card = getFirstCard(node, node.slug);
    }
  }
 
  return card;
}

/**
 * functionality to deal with next and previous navigations
 * @param {any} rootNode
 * @param {any} curSufix
 */
export function getPrevNext( rootNode, curSufix ) {
    var listOfUrls = [];
    let generateAllUrls = function( rootNode, prefix ) {
        // Generate all sets of urls for all cards
        for ( var i = 0; i < rootNode.listOfCards.length; i++ ) {
            if(rootNode.listOfCards[i]['display'] && rootNode.listOfCards[i]['display'] == false)
            continue;
            else{
              let pre_url = (prefix.includes("maxdepth"))?prefix:prefix + rootNode.listOfCards[i]['slug']
              listOfUrls.push(pre_url);
            }
        }
        for ( var i = 0; i < rootNode.listOfNodes.length; i++ ) {
        if(rootNode.listOfNodes[i]["Depth Of Tree 3"]!=undefined){
          for(let j=0;j<Object.keys(rootNode.listOfNodes[i]).length;j++){
            if(Object.keys(rootNode.listOfNodes[i])[j].includes("Depth Of Tree"))
              generateAllUrls(rootNode.listOfNodes[i][Object.keys(rootNode.listOfNodes[i])[j]] , rootNode.listOfNodes[i].slug +"/"+ rootNode.listOfNodes[i][Object.keys(rootNode.listOfNodes[i])[j]].slug)
          }
        }else{
            generateAllUrls( rootNode.listOfNodes[i], prefix + rootNode.listOfNodes[i]["slug"] + "/" );
        }
    }
  }
    //when listofNodes is empty append slug to prefix
    if(rootNode.listOfNodes.length == 0){
    	var rootSlug = curSufix.split("/")
    	generateAllUrls( rootNode, rootSlug[0]+"/");
    }
    else generateAllUrls( rootNode, "" );

    var curIndex = listOfUrls.indexOf( curSufix );
    var prev = null;
    var next = null;
    if ( curIndex > 0 ) {
        prev = listOfUrls[curIndex - 1];
    }
    if ( curIndex < listOfUrls.length - 1 ) {
        next = listOfUrls[curIndex + 1]
    }

    return {
        "prev": prev,
        "cur": curSufix,
        "next": next
    };


}

export function getLastCardOfTree(output){
if(output.listOfNodes.length!=0){
  output= output.listOfNodes[output.listOfNodes.length-1];
}
  if(output.listOfNodes.length>0){
    return getLastCardOfTree(output);

  }
  else{
    return output.listOfCards[output.listOfCards.length - 1];
  }
}

export function fetchMaxDepthCard(node){
  return node.listOfCards[0];
}