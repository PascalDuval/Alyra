pragma solidity ^0.5.7;



// 4.2.2
//  Écrire la version complète du contrat Crédibilité avec les fonctions suivantes :
// Une fonction pure produireHash(string memory url) qui prend en paramètre une chaîne de caractères 
// et retourne le condensat keccak256 au format bytes32.
// [aide: vous devrez convertir la chaine de caractères fournie en format bytes avec bytes()]
//   Une fonction transfer(address destinataire, uint256 valeur) qui permet de transférer ses “cred”. 
// Petite particularité, les creds peuvent uniquement être transférés à d’autres détenteurs de cred 
// et en gardant toujours au moinsun cred.
// [aide: la première ligne de la fonction peut être : require(cred[msg.sender] > valeur); avec une inégalité stricte]
// Une fonction remettre(bytes32 dev) qui prend en paramètre le hash du devoir et retourne l’ordre d’arrivée.

// 4.2.3 
// on ajoute des événements
// Ajouter à Crédibilité un événement qui pour chaque remise de devoir indique le hash du devoir et l’adresse de celui qui l’a remist.
// Lire depuis l’interface chaque remise de devoir et l’afficher dans la console.
// (optionnel) Afficher les remises de devoir dans l’interface.



contract Credibilite {
  
//   using SafeMath for uint256;
  
   mapping (address => uint256) public cred;
   bytes32[] private devoirs;
   event Devoir(bytes32 dev, address adr);
   
   
   uint256 public ordre; // orde actuel 




function produireHash(string memory url)  public pure returns (bytes32)  {
    return keccak256(bytes(url));
    }    

function transfererCred (address destinataire, uint256 valeur) public {
    require(cred[msg.sender] > valeur, "Vous devez avoir plus que le nombre de creds que vous cédez");
    require(cred[destinataire] > 0, "Le destinaire doit avoir des creds");
    cred[msg.sender] -= valeur; 
    cred[destinataire] += valeur; // destinataire.transfer(valeur); ?
    }
    
 function remettre(bytes32 dev) external returns (uint){
    ordre = devoirs.push(dev);
    if (ordre == 1) {
    cred[msg.sender] = 30;     
    }
    if (ordre == 2) {
    cred[msg.sender] = 20;     
    }
   if (ordre > 2) {
    cred[msg.sender] = 10;     
    }
emit Devoir(dev, msg.sender);  // déclenche l’événement avec le mot clé emit et les informations correspondantes    
return ordre;    
}
    
    
}