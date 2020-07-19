pragma solidity ^0.4.21;


import "https://github.com/PascalDuval/Alyra/blob/master/7-1-7.sol"; 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/math/SafeMath.sol";

contract bazarEF {
   using SafeMath for uint256;
    ApollinaireToken private ObjetalaVenteEH;

    event NewEnchere(uint256 id, uint256 finEnchere, uint256 objet, address vendeur);
    
    constructor() public {
        ObjetalaVenteEH = ApollinaireToken(0xBCbFe3d91e3346854B25A554E5f278dEaa8eE452); // à remplacer
        }


    
    uint256 constant DELAI = 3 * (10**4); // 50 blocs à raison de 10 * 60 secondes par bloc en moyenne soit 500 minutes soit 8.3 heures
    // uint256 constant START_BLOCK = block.number;
    uint constant PAS = 1; // diminution de 1% du prix initial fixé par le vendeur par bloc ..
    
    struct Enchere {
    address meilleurAcheteur;
    uint256 meilleureOffre;
    uint256 finEnchere; // il faut quand même qu'il y ait une fin. On arrête quand le prix descend à la moitié du prix (cf. DELAI)
    uint256 objet;
    uint256 prixdepart;
    uint256 startblock;
    address vendeur;
    }

   Enchere[] public encheres;  ///tableau des enchères
   
   
   // Proposer à la création d’une offre le choix entre deux mécanismes d’enchères: 
   // Classique ou hollandaise. 
   // Le prix sera alors proposé initialement par le vendeur, 
   // et réduit par une formule en fonction du bloc auquel l’acheteur se propose (par exemple réduit de 0.1% du prix initial par bloc, cette valeur peut être stockée comme valeur constante au moment de la proposition). 
   // Dès que l’acheteur se propose, l’objet lui est attribué.

    
   enum TypeEnchere { CLASSIQUE, HOLLANDAISE }
   TypeEnchere typeEnchere;
   TypeEnchere typeenchere = TypeEnchere.HOLLANDAISE;
   function ChooseHollandaise() public view returns (uint){
   return uint(typeenchere);
   }


   
    
    // function proposerALaVente(uint256 _objet, uint _choix, uint256 _price) external  {
        
    function proposerALaVente(uint256 _objet, uint256 _price) external  {    
    // require(ObjetalaVenteEH.exists(_objet), "cet objet n'existe pas"); 
    // require((ChooseHollandaise() == _choix), "ce contrat n'effectue que des enchères hollandaises - taper 1 dans le choix"); 
    
     //require(_price.div(10000).mul(10000) == _price, "le prix de départ minimum doit être de 10000");
     address owner = ObjetalaVenteEH.ownerOf(_objet);  // récupérer l'adresse de celui qui détient l'objet)  
     address spender = msg.sender;  // récupérer le spender qui éventuellement opère pour le owner
     // require (spender == owner || ObjetalaVenteEH.getApproved(_objet) == spender || ObjetalaVenteEH.isApprovedForAll(owner, spender));
     
     require (spender == owner, "vous n'êtes pas le propriétaire de cet objet"); 
    
     address meilleurAcheteur = address(0); // initialisation
     uint256 meilleureOffre = 0; // initialisation
     uint256 finEnchere = block.timestamp.add(DELAI); // récuper la date de la fin de l'enchère qui s'arrête nécessairement "assez tôt"
     
     
     uint256 prixdepart = _price; // le prix de départ est fixé par celui qui propose l'enchère
     // uint256 startblock = START_BLOCK;
     
     uint256 startblock = block.number;
     
     uint256 id = encheres.push(Enchere(meilleurAcheteur,meilleureOffre,finEnchere,_objet,prixdepart,startblock,spender)) -1; 
     
     // on doit transférer l'objet au contrat
     ObjetalaVenteEH.approve(address(this), _objet); // il faut déjà l'approuver...
     ObjetalaVenteEH.safeTransferFrom(spender, address(this), _objet);
     
	 emit NewEnchere(id, finEnchere, _objet, spender);	
    }


    
    function getCurrentPrice(uint indice) public view returns(uint256) {
        Enchere storage PriceEnchere = encheres[indice];
        uint256 currentbloc = block.number;
        uint256 n = currentbloc.sub(PriceEnchere.startblock);
        uint256 newpourcentage = PAS.mul(n).mul(100);
        uint256 minus =  PriceEnchere.prixdepart.mul(newpourcentage).div(10000);
        
        uint256 montantcourrant = PriceEnchere.prixdepart.sub(minus);
        return montantcourrant;

    }


      mapping (address => mapping (uint256 => uint256)) public soldes;  // mapping des remboursements pour telle adresse et telle enchère

      function offre(uint indice)  public payable { // l'indice est le numéro d'enchère
      Enchere storage encoursEnchere = encheres[indice]; 
      
      
      //uint256 datelimite = encoursEnchere.finEnchere;
      bool EnCours = (block.timestamp <= encoursEnchere.finEnchere); // est-ce qu'elle est toujours en cours ? 
      require(EnCours, "L'enchère est close !");
      
      uint256 montantnouvelleOffre = getCurrentPrice(indice);
      
      require((montantnouvelleOffre < encoursEnchere.prixdepart), "Attendre quelques bocs que le prix diminue..") ; // normalement pas besoin
      require((msg.sender != encoursEnchere.vendeur), "Vous êtes le vendeur de cet objet ! et vous avez fixé le prix de départ.."); // on ne permet pas que ce soit le vendeur lui-même qui fasse une offre
      require((msg.sender != encoursEnchere.meilleurAcheteur), "Vous êtes déjà le meilleur acheteur"); // on vérifie aussi qu'il ne sous-enchérit pas sur lui-même

      address(this).transfer(montantnouvelleOffre); // on verse au contrat pour que le vendeur puisse récupérer le prix de l'enchère ensuite
      
    
      
      encoursEnchere.meilleurAcheteur = msg.sender;      // mise à jour de l'enchère avec ce meilleur Acheteur
      encoursEnchere.meilleureOffre = montantnouvelleOffre;
      encoursEnchere.finEnchere = block.timestamp; // fermer l'enchère avec block.timestamp !!!!!! 
      
      
        // cet acheteur doit pouvoir récupérer immédiatement l'objet
      ObjetalaVenteEH.safeTransferFrom(address(this), msg.sender, encoursEnchere.objet);
      

      
      soldes[encoursEnchere.meilleurAcheteur][indice] =  montantnouvelleOffre;  // pour pouvoir gérer plusieurs enchères sur plusieurs objets
      
      
      

    }


    function solde(uint256 _indice) public  { // permet au vendeur de récupérer le prix de l'enchère
        require(!(soldes[msg.sender][_indice] == 0), "Aucun solde d'enchère à cette addresse pour cet objet .. ");
        uint256 enchereaverser = soldes[msg.sender][_indice];
        msg.sender.transfer(enchereaverser);
                
    }
    

   


} 
