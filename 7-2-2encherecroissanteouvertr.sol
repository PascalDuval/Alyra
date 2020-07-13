pragma solidity ^0.4.21;


import "https://github.com/PascalDuval/Alyra/blob/master/7-1-7.sol"; 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/math/SafeMath.sol";

contract bazar {
   using SafeMath for uint256;
   
   // address payable plateforme;
   

    ApollinaireToken private ObjetalaVente;

    event NewEnchere(uint256 id, uint256 finEnchere, uint256 objet, address vendeur);
   
    constructor() public {
        // magicItemContract = 0x1593EA08781d98C8Ef5109D7aEF7708c2f3880E4; 
        ObjetalaVente = ApollinaireToken(0xBE1fD0131aF48Ba1cC80036d5E53F1AA4513a138); // à remplacer
        // plateforme  = msg.sender;
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
     address owner = ObjetalaVente.ownerOf(_objet);  // récupérer le Vendeur (c'est celui détient l'objet)  
     address spender = msg.sender;  // récupérer le spender qui éventuellement opère pour le owner
    
    // il faudrait faire plutôt d'après les spécifications
    // require (vendeur == address(this), "cet objet n'a pas été transféré au contrat ")
    
    // Mais on peut se demander si c'est pas transféré la propriété préalablement dans le contrat ApollinaireToken 
    // cela se fait en faisant un safeTranferFrom(this.address) après avoir donné les autorisations
    
     require (spender == owner || ObjetalaVente.getApproved(_objet) == spender || ObjetalaVente.isApprovedForAll(owner, spender));
     
     // on va se contenter dans un premier temps de vérifier si le spender est msg.sender est  approuvé ou est opérateur.
     // de plus on va se limiter à la première condition pour nos tests.
     
     address meilleurAcheteur = address(0);
     uint256 meilleureOffre = 0;
     uint256 finEnchere = block.timestamp.add(DELAI); // récuper la date de la fin de l'enchère
     uint256 id = encheres.push(Enchere(meilleurAcheteur,meilleureOffre ,finEnchere, _objet, spender)) -1; 
	 emit NewEnchere(id, finEnchere, _objet, spender);	
    }

      // mapping (address  => uint256) public remboursements; // mapping des remboursements
      
      mapping (address => mapping (uint256 => uint256)) public remboursements;  // mapping des remboursements pour telle adresse et telle enchère

      function offre(uint indice)  public payable { // l'indice est le numéro d'enchère
      Enchere storage encoursEnchere = encheres[indice]; 
      // il faudrait vérifier qu'elle existe..
      
      uint256 datelimite = encoursEnchere.finEnchere;
      bool EnCours = (block.timestamp <= datelimite); // est-ce qu'elle est toujours en cours ? 
      require(EnCours, "L'enchère est close !");
      
      uint256 montantnouvelleOffre = msg.value;
      uint256 montantOffreEncours =  encoursEnchere.meilleureOffre;

      require((msg.sender != encoursEnchere.vendeur), "Vous êtes le vendeur de cet objet ! le prix de départ est 0 par défaut"); // on ne permet pas que ce soit le vendeur lui-même qui fasse une offre
      require((montantnouvelleOffre > montantOffreEncours), "Une meilleure offre a été faite pour cet objet !") ;
      require((msg.sender != encoursEnchere.meilleurAcheteur), "Vous êtes déjà le meilleur acheteur"); // on vérifie aussi qu'il ne renchérit pas sur lui-même

      remboursements[encoursEnchere.meilleurAcheteur][indice] =  montantOffreEncours;  // pour pouvoir gérer plusieurs enchères sur plusieurs objets
        
      encoursEnchere.meilleurAcheteur = msg.sender;      // mise à jour de l'enchère avec ce meilleur Acheteur
      encoursEnchere.meilleureOffre = montantnouvelleOffre; // mise à jou de l'enchère avec ce nouveau montant

    }

    function remboursement(uint256 _indice) public  {
        address ToAncientAcheteur = msg.sender;
        // require(!(remboursements[ToAncientAcheteur] == 0), "Aucun remboursement n'est prévue à cette addresse... ");
        require(!(remboursements[ToAncientAcheteur][_indice] == 0), "Aucun remboursement prévue à cette addresse pour cet objet .. ");
        // uint256 AncienneOffre = remboursements[ToAncientAcheteur];
        uint256 AncienneOffre = remboursements[ToAncientAcheteur][_indice];
        ToAncientAcheteur.transfer(AncienneOffre);
                
    }
    
   

    function recupererObjet(uint256 _indice) public {
     Enchere storage FinalEnchere = encheres[_indice]; 
      uint256 datelimite = FinalEnchere.finEnchere;
      require(block.timestamp >= datelimite, "l'enchère n'est pas encore close !"); 
      uint256 ObjetArecuperer = FinalEnchere.objet;
      address vainqueur =  FinalEnchere.meilleurAcheteur;// récupérer le meilleur acheteur
      require(vainqueur == msg.sender, "vous n'êtes pas habilité à récupérer cet objet");
      address vendeur =  FinalEnchere.vendeur;// récupérer le meilleur acheteur
      
      // À la fin de l’enchère, l’acheteur le mieux offrant peut appeler la fonction récupererObjet(uint indice) . 
      // S’il n’a pas trouvé preneur, le vendeur peut le récupérer.
      
      if(vainqueur == address(0)) { // retour au vendeur
       // ObjetalaVente.safeTransferFrom(address(this), vendeur, ObjetArecuperer); // si on a effectivement fait un transfert préalablement (mais ce n'est peut-être pas souhaitable), on effectue le transfert dans l'autre sens
      }
      else {
        ObjetalaVente.safeTransferFrom(vendeur, vainqueur, ObjetArecuperer);  
       // ObjetalaVente.safeTransferFrom(address(this), vainqueur, ObjetArecuperer); // si on a effectivement fait un transfert préalablement (mais ce n'est peut-être pas souhaitable), on effectue le transfert dans l'autre sens
        
      }
     
 
      }


} 
