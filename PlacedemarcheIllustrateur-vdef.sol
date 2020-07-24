pragma solidity >=0.6.0;

import "github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol"; 
// import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol";

 pragma experimental ABIEncoderV2;  

contract PdmIllustrateurs {
    
    
    using SafeMath for uint256;
   
    address payable plateforme;

    constructor() public  {
        plateforme  = msg.sender;
    }
    

	struct Illustrateur {
		string nom;	        // "Prénom Nom" de l'illustrateur
		// uint8 reputation; 	// Réputation va jusqu'à 255
		mapping (address => uint8) reputation; // balance de reputaton dont dispose une addresse illustrateur
		string portfolio; //site ou url du portfolio de cet illustrateur pour 
		bytes32 hashremis; // hashremis pour une offre dont il est le candidat retenu
		string url; // new 06/05/2020
	}



	mapping (address  => Illustrateur) Illustrateurs;
	
	address payable[]  public IllustrateurComptes;
	
    // address payable[] public Users; //mapping des adresses payables pazs nécessaires
    
	mapping (address => bool) public illustrateurMembre;
	
    
    enum statutDemande { OUVERTE, ENCOURS, FERMEE }
    
    uint8 constant MAX_REPUTATION = 255;   // Reputation maximale
    uint32 constant MAX_DELAI = 52 weeks;   // Delai maximal en secondes = 1 an
    uint32 constant MIN_DELAI = 2 days;    // Delai minimal en secondes = 2 jours
    uint256 constant MIN_REMUNERATION = 30000;   // minumum de la rémunération en wei
    uint32 constant MIN_DESCRIPTION = 10;   // longueur minimale (en bytes) d'une description (un octet = 1 char)
    uint32 constant MAX_DESCRIPTION = 1000;   // longueur maximale (en bytes) d'une description (une page)
    
    
    struct Demande {
        address entreprise;	    // adresse de l'entreprise demandeuse
    	uint256 remuneration;	// en wei
		uint32 delai;			// en secondes à partir de l'acceptation
		string description;		// description de la tâche à effectuer
		uint8  min_reputation;	// réputation minimum pour postuler
		statutDemande statut;   // statut de la de la demande
		address[] candidats;    // renseigner au moment de postuler
		uint8 numero_candidat;  // numero du candidat à qui est attribuée l'offre (indice dansle tableau)
		bytes32 hashtravailremis; // hash du travail remis 
		uint256 date;           // il faut une date
		string url;             // il faut une url
	}
	
   mapping (bytes32 => Demande) Demandes;
   bytes32[] public TabDemandes; 
   

    // new 
    event InscriptionIllustrateurok(address illustrateur, string nom);
	function inscriptionIllustrateur(string memory _nom, string memory _portfolio) public {
	    
	// il ne faut pas oublier de la déclarer en payable new 07/06/2020 euh non !    
	
	//address payable addressillustrateur = msg.sender;
	address payable addressillustrateur = msg.sender;
	
	// ajout
	// address payable user = msg.sender;
	
	require(!illustrateurMembre[addressillustrateur], "Ce compte existe déjà  !");
	// on crée un nouvel utilisateur avec la clé du mapping 
	Illustrateur storage illustrateur = Illustrateurs[addressillustrateur];
	
	
	// on renseigne la structure
	illustrateur.nom = _nom; // avec le nom
	illustrateur.portfolio = _portfolio;  // avec le portfolio
	illustrateur.reputation[addressillustrateur] = 1;  // avec la reputation -> 1 à l'initialisation
	
	
	IllustrateurComptes.push(addressillustrateur);
	
	// on maintient deux tables ...  Users.push(user);
	
	
	illustrateurMembre[addressillustrateur] = true; // on met à jour 
    emit InscriptionIllustrateurok(msg.sender, _nom); 
	}

    
    function getIllustrateurs()  public view returns(address payable[] memory ) {
	return  IllustrateurComptes; 
	 }

	function getReputIllustrateur(address _address) view public returns (uint8) {
 
	require(illustrateurMembre[_address], "Ce compte illstrateur n'existe pas !");
	Illustrateur storage illustrateur = Illustrateurs[_address]; 
	
	return  (illustrateur.reputation[_address]);
	}

    // new 05/06/2020
    function getIllustrateurinfo(address _address) view public returns (string memory, uint8, string memory) {
	require(illustrateurMembre[_address], "Ce compte n'existe pas !");
	Illustrateur storage illustrateur = Illustrateurs[_address]; 
	return  (illustrateur.nom, illustrateur.reputation[_address], illustrateur.portfolio);
	}

    // new 06/06/2020
    function getIllustrateurtravail(address _address) view public returns (bytes32, string memory) {
	require(illustrateurMembre[_address], "Ce compte n'existe pas !");
	Illustrateur storage illustrateur = Illustrateurs[_address]; 
	return  (illustrateur.hashremis, illustrateur.url);
	}


    // changer le type de public à internal
    function addReputIllustrateur(address _address) public  returns (uint8) {
  	require(illustrateurMembre[_address], "Ce compte n'existe pas !");
	// Illustrateurs[_address].reputation +=1;
	Illustrateur storage illustrateur = Illustrateurs[_address];	
	illustrateur.reputation[_address] += 1; 
	
	// return  (Illustrateurs[_address].reputation);
	return  (illustrateur.reputation[_address]);
    }

    // new 06/06/2020
    event TransReputok(address donateur, uint8 credit, address recepteur);
    function TransReputIllustrateur(address _address, uint8 _cred) public  {
  	require(illustrateurMembre[msg.sender], "Ce compte illustrateur n'existe pas - enregistrez-vous d'abord !");
  	require(illustrateurMembre[_address], "Ce compte illustrateur n'existe pas !");
	
	Illustrateur storage illustrateurAcrediter = Illustrateurs[_address];	
	require	(illustrateurAcrediter.reputation[_address] != MAX_REPUTATION, "Ce compte a déjà la réputation maximale");
	
	Illustrateur storage illustrateurTodebiter = Illustrateurs[msg.sender];
	require	(illustrateurTodebiter.reputation[msg.sender] >= _cred, "Ce compte n'a pas de credit réputation suffisant"); //possibilité de solder son adresse
	
	illustrateurTodebiter.reputation[msg.sender] -= _cred; 
	illustrateurAcrediter.reputation[_address] += _cred; 
	emit TransReputok(msg.sender, _cred, _address); // msg_sender Attention possibilité de solder!!
    }

    event InscriptionDemandeok(address entreprise, uint256 remuneration, uint32 delai, string description, uint8 min_reputation);
   
//   uint256 frais;
//   uint256 remu;
//   uint256 coutotal;
   
    function ajouterDemande(uint256 _remuneration, uint32 _delai, string memory _description, uint8 _min_reputation)  public payable
	{
	    
    // vérifier le msg.sender
	address _entreprise = msg.sender;
	
	
	require(msg.value >= _remuneration, "Vous n'avez pas les fonds nécessaires"); 
	// renseigner dans le javascript
	
	require(_remuneration >= MIN_REMUNERATION, "La rémunération ne peut être inférieur à 30000 wei");     
	require(_min_reputation <= MAX_REPUTATION, "La réputation minimale demandée ne peut être supérieure à 255");  

	
	require((_delai <= MAX_DELAI && _delai >= MIN_DELAI), "Le délai maximal pour toute demande est d'un an - le délai minimal est de deux jours"); 
	
    bytes memory fttb = abi.encodePacked(_entreprise,  _remuneration, _delai, _description, _min_reputation); //mettre la date ?
    bytes32 hashDemande = keccak256(bytes(fttb)); 

    Demande storage CastDemande = Demandes[hashDemande]; 

    require(!demandeExiste(hashDemande), "Cette demande existe déjà");
    CastDemande.entreprise = _entreprise;
    
    CastDemande.remuneration = _remuneration; 
    // CastDemande.frais = frais; // celui-ci est versé tout de suit ou à la fin dans le solde des opérations
    CastDemande.delai = _delai;
    CastDemande.description = _description;
    CastDemande.min_reputation = _min_reputation;
    CastDemande.statut = statutDemande.OUVERTE;
    CastDemande.numero_candidat = 0; // au début il n'y a pas de candidat valide.
    
    CastDemande.date = block.timestamp ; // il faut la date !
    
    TabDemandes.push(hashDemande);
   
    // uint256 frais = _remuneration.mul(2).div(100);
    // coutotal = _remuneration.add(frais);
    
    
    
    emit InscriptionDemandeok(_entreprise,  _remuneration, _delai, _description, _min_reputation);
    
   	}
   	

    function listerDemandes() public view returns (Demande[] memory) { // peut être fait au niveau HTML
        uint256 n = TabDemandes.length;
        // Demande storage listeDemandes ; 
        Demande[] memory listeDemandes = new Demande[](n);
                // Demande storage listeDemandes = new Demande[](n);
        for (uint256 i=0 ; i< n ; i++) {
            Demande memory d = afficherDemandebis(TabDemandes[i]);
            //Demande memory d = Demandes[h];
            listeDemandes[i] = d;
        }
        return listeDemandes;
	}
	
    function getHashDemande(uint256 _numDemande) public view returns(bytes32) {
    return TabDemandes[_numDemande];
    // retourne le Hash d'une demande par son numéro
    }	

    function afficherDemande(bytes32 _hash) view public returns (address, uint256, uint8, uint256, string memory, statutDemande, uint256) { 
    return(Demandes[_hash].entreprise, Demandes[_hash].remuneration, Demandes[_hash].min_reputation, Demandes[_hash].delai, Demandes[_hash].description, Demandes[_hash].statut, Demandes[_hash].date);
    } // retourne simplement les données pour un hash donné



    function afficherDemandebis(bytes32 _hashDemande) public view returns (Demande memory) {
    Demande memory demande = Demandes[_hashDemande];
    require(demandeExiste(_hashDemande), "Cette demande n'existe pas");
    return demande;
	}
	
    function nbredemandes() public view returns(uint256)
    {
    return TabDemandes.length;    
    }



    function demandeExiste(bytes32 hashDemande) public view returns (bool) {
	    return Demandes[hashDemande].remuneration > 0;  // on fait un simple test sur la rémunération
	}  	

    event Postulationok(address Illustrateur, bytes32 offre);
    function postuler(bytes32 _hashDemande) public returns (bytes32)  {
        address Postulant = msg.sender;
 
        Demande storage Postule = Demandes[_hashDemande]; 
        require(getReputIllustrateur(Postulant) >= Postule.min_reputation, "Votre réputation n'est pas suffisante !"); // ici il faut vérifier que sa reputation est supérieure à celle de la demande.. 
        
        Postule.candidats.push(Postulant); // Il a un numéro d'entrée déterminé par sa position dans le tableau d'adresse
        emit  Postulationok(Postulant,  _hashDemande);
        return _hashDemande;
      	}
      	
    event accepterOffreok(bytes32 offre, statutDemande);
    function accepterOffre(address _Postulant, bytes32 _hashDemande) public  returns (address, statutDemande, bytes32) {
        Demande storage Offre = Demandes[_hashDemande]; // var Offre = Demandes[_hashDemande] deprecated
        require(Offre.entreprise == msg.sender, "Vous n'êtes pas l'emetteur de cette offre !");
      	require((Offre.numero_candidat ==0), "Un candidat est déjà validé pour cette demande"); 
        
        uint8 numero = 0; // on va chercher le numéro de ce candidat...
        for (uint8 i = 0; i < Offre.candidats.length; i++) {
            if (Offre.candidats[i] == _Postulant) {
            numero = i+1;
            break;  //on sort  dès qu'on l'a trouvé
            }
      	} // fin du for
      	require(numero !=0, "Cette adresse n'a pas postulé pour cette demande");
        Offre.numero_candidat = numero; //  renseigner le numero de candidat : il devient actif et validé 
      	Offre.statut = statutDemande.ENCOURS; // mettre à jour la demande
      	emit accepterOffreok(_hashDemande, Offre.statut);
        return (_Postulant, Demandes[_hashDemande].statut, _hashDemande);
      	} 
      	
    
    mapping (bytes32 => bool) public TravauxMap;
      	
    function produireHash(string memory url) pure internal  returns (bytes32) {
    return keccak256(bytes(url));
    }  	
    
    event livraisonok(address illustrateur, bytes32 hashtravail);
    function livraison (string memory _url, bytes32 _demande) public returns (bytes32) {
      require(illustrateurMembre[msg.sender], "Ce compte n'existe pas !");
      Demande storage Travail = Demandes[_demande];    
      // à la place de memory new 05/06/2020
      require(Travail.hashtravailremis.length != 0, "Hash du travail déjà remis !"); // il faut qu'aucun travail ne soit remis
      require(Travail.statut == statutDemande.ENCOURS, "Il faut que la demande soit en cours"); 
      bytes32 livrable = produireHash( _url);
      
      require(!TravauxMap[livrable], "Ce hash existe déjà  !");
      
      // verification que le délai n'est pas dépassé
      uint256 datelimite = Travail.date.add(Travail.delai);
      bool Intime = (block.timestamp <= datelimite); 
      
      require(Intime, "Le délai est dépassé");
      // assert (Intime);

      Travail.hashtravailremis = livrable; // on le dépose une fois chez l'entreprise
      Travail.url = _url;
      
     Illustrateur storage illustrateur = Illustrateurs[msg.sender];
     illustrateur.hashremis = livrable; // et une autre fois chez l'illustrateur;
     illustrateur.url = _url;
     
     TravauxMap[livrable] = true; // et on met à jour la table des Travaux
     
      
     addReputIllustrateur(msg.sender);
      
   
    emit livraisonok(msg.sender, Travail.hashtravailremis);
    return livrable;
    }
  
  
  
  
    function afficherUrlTravail(bytes32 _hashDemande) public view returns (string memory) {
    Demande memory demande = Demandes[_hashDemande];
    require(demandeExiste(_hashDemande), "Cette demande n'existe pas");
    return demande.url; // utile pour accepter la livraison ...
	}
  
  
   
 
    event accepterlivraisonok(string url, bytes32 travail,statutDemande);    
    // event accepterlivraisonok(address payable, address payable, uint256 amount);    
    function acceptelivraison (address _illustrateur, bytes32 _demande) public returns (bytes32) {
    Demande storage Livraison = Demandes[_demande];    
    require(Livraison.entreprise == msg.sender, "Vous n'êtes pas l'emetteur de cette offre !");
    
    require(Livraison.statut == statutDemande.ENCOURS, "La demande n'est pas en cours - il faut sélectionner déjà un candidat !");
    require(Livraison.hashtravailremis.length != 0, "Aucun travail remis!");  // il faut qu'aucun travail ne soit remis
    
    
    
    // on vérifie en outre que c'est le même hash de travail remis côté du côté illustrateur
    Illustrateur storage illustrateur = Illustrateurs[_illustrateur];	
	require	(illustrateur.hashremis == Livraison.hashtravailremis, "Aucun hash correspondant côté illustrateur");
    
    
    Livraison.statut = statutDemande.FERMEE;
    
    addReputIllustrateur(_illustrateur);
     

    address payable illustrateurAddress = IllustrateurComptes[Livraison.numero_candidat -1];
    uint256 salairebrut = Livraison.remuneration;
    
    uint256 frais = salairebrut.mul(2).div(100);
    uint256 salairenet = salairebrut.sub(frais);

    illustrateurAddress.transfer(salairenet);
    
   
    
    emit accepterlivraisonok(Livraison.url, Livraison.hashtravailremis, Livraison.statut);
    // emit accepterlivraisonok(plateforme, illustrateurAddress, salaire);

    return Livraison.hashtravailremis;
    }




// function ownerRestitue(address payable _illustrateurAddress, uint256 _salaire) internal   {
//        address payable illustrateur = _illustrateurAddress;
//        illustrateur.transfer(_salaire);
//    }


} // fin contract