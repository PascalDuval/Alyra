pragma solidity ^0.4.21;


import "https://github.com/PascalDuval/Alyra/blob/master/7-1-7.sol"; 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/math/SafeMath.sol";

contract bazar {
   using SafeMath for uint256;
   
   
   

    ApollinaireToken private ObjetalaVente;

    event NewEnchere(uint256 id, uint256 finEnchere, uint256 objet, address vendeur);
   
    constructor() public {
        // magicItemContract = 0x1593EA08781d98C8Ef5109D7aEF7708c2f3880E4; 
        ObjetalaVente = ApollinaireToken(0x1593EA08781d98C8Ef5109D7aEF7708c2f3880E4); // à remplacer
}


    uint256 constant DELAI = 6 * (10**5); // 1000 blocs à raison de 10 * 60 secondes par bloc 
    
    struct Enchere {
     address meilleurAcheteur;
     uint256 meilleureOffre;
     uint256 finEnchere;
     uint256 objet;
     address vendeur;
    }

   Enchere[] public encheres;  ///tableau des enchères

    function proposerALaVente(uint256 _objet) external  {
    require(ObjetalaVente.exists(_objet), "cet objet n'existe pas"); 
    address vendeur = ObjetalaVente.ownerOf(_objet);  // récupérer le Vendeur (c'est celui détient l'objet)
    require (msg.sender == vendeur ||  ObjetalaVente.getApproved(_objet) == msg.sender ||  ObjetalaVente.isApprovedForAll(vendeur, msg.sender));
       
       address meilleurAcheteur = address(0);
       uint256 meilleureOffre = 0;
       uint256 finEnchere = block.timestamp.add(DELAI); // récuper la date de la fin de l'enchère
       uint256 id = encheres.push(Enchere(meilleurAcheteur,meilleureOffre ,finEnchere, _objet, vendeur)) -1; 
	   emit NewEnchere(id, finEnchere, _objet, vendeur);	
    }

} 
