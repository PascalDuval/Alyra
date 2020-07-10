pragma solidity ^0.4.19;
pragma experimental ABIEncoderV2;  



/// Les sept épées
/// @ notice en hommage à Guillaume Guillaume APOLLINAIRE
///Recueil : "Alcools"

///    La première est toute d’argent
///    Et son nom tremblant c’est Pâline
///    Sa lame un ciel d’hiver neigeant
///    Son destin sanglant gibeline
///    Vulcain mourut en la forgeant

///    La seconde nommée Noubosse
///    Est un bel arc-en-ciel joyeux
///    Les dieux s’en servent à leurs noces
///    Elle a tué trente Bé-Rieux
///    Et fut douée par Carabosse

///    La troisième bleu féminin
///    N’en est pas moins un chibriape
///    Appelé Lul de Faltenin
///    Et que porte sur une nappe
///    L’Hermès Ernest devenu nain

///    La quatrième Malourène
///    Est un fleuve vert et doré
///    C’est le soir quand les riveraines
///    Y baignent leurs corps adorés
///    Et des chants de rameurs s’y trainent

///    La cinquième Sainte-Fabeau
///    C’est la plus belle des quenouilles
///    C’est un cyprès sur un tombeau
///    Où les quatre vents s’agenouillent
///    Et chaque nuit c’est un flambeau

///    La Sixième métal de gloire
///    C’est l’ami aux si douces mains
///    Dont chaque matin nous sépare
///   Adieu voilà votre chemin
///    Les coqs s’épuisaient en fanfares

///    Et la septième s’exténue
///    Une femme une rose morte
///    Merci que le dernier venu
///    Sur mon amour ferme la porte
///    Je ne vous ai jamais connue

// import "./ownable.sol";
// import "./ERC721simple.sol";

// contract ApollinaireFactory is ERC721simple {

    contract ApollinaireFactory  {


  string[10][] public magicwords;
 
    constructor() public {
        /// @notice tableau des mots magiques  
        magicwords.push(["Pâline ","Noubosse ", "Lul de Faltenin ", "Malourène ", "Sainte-Fabeau ", "Chrindrono ", "Annie Playden ", "Lou ","Marie Laurencin ","Madeleine "]); 
        magicwords.push(["Vulcain ", "Carabosse ", "Hermes ", "Avelia ", "Ezheia ", "Naena ", "Eros ", "Eros ", "Eros ", "Eros "]);  
        magicwords.push(["Argent ", "arc-en-ciel ", "bleu féminin ", "fleuve vert et doré ", "Gold ", "métal de gloire ", "Améthyste ", "Saphir ", "Rubis ", "Larmes "]);
        magicwords.push(["gibeline ", "noces ", "chibriape ", "riveraines ", "quenouilles ", "C’est l’ami aux si douces mains ", "C’est un cyprès sur un tombeau ", "fanfare ", "dernier venu ", "mal aimé" ]);
    }
    
    
  function getMagicNom(uint _index) internal view returns (string memory) {
        return magicwords[0][_index]; 
    }
    
  function getMagicDivtut(uint _index) internal view returns (string memory) {
        return magicwords[1][_index];     }

  function getMagicMatcoul(uint _index) internal view returns (string memory) {
        return magicwords[2][_index]; 
    }

  function getMagicEvoc(uint _index) internal view returns (string memory) {
        return magicwords[3][_index]; 
    }

  function getMagicNomFromBlason(uint _blason) internal view returns (string memory) {
        uint indexnom = _blason / 1000;
        string memory nom =  getMagicNom(indexnom);  
        return nom; 
    }

 function getMagicDivtutFromBlason(uint _blason) internal view returns (string memory) {
        uint indexdivtut = (_blason - ((_blason / 1000) * 1000)) / 100;
        string memory div =  getMagicDivtut(indexdivtut);  
        return div; 
    }

 function getMagicMatcoulFromBlason(uint _blason) internal view returns (string memory) {
        uint nbremilliers  = _blason / 1000;
        uint nbrecentaines  = (_blason - (nbremilliers * 1000)) / 100;
        uint nbredizaines = (_blason - (nbremilliers * 1000) - (nbrecentaines * 100)) / 10;
        uint indexmatcoul = nbredizaines; 
        string memory coul =  getMagicMatcoul(indexmatcoul);  
        return coul; 
    }

 // 
 function getMagicEvocFromBlason(uint _blason) internal view returns (string memory) {
        uint nbremilliers  = _blason / 1000;
        uint nbrecentaines  = (_blason - (nbremilliers * 1000)) / 100;
        uint nbredizaines = (_blason - (nbremilliers * 1000) - (nbrecentaines * 100)) / 10;
        uint nbrunites = _blason - (nbremilliers * 1000) - (nbrecentaines * 100) - (nbredizaines * 10);
        uint indexevoc = nbrunites; 
        string memory evoc =  getMagicEvoc(indexevoc);  
        return evoc; 
    }

    function append(string a, string b, string c, string d) internal pure returns (string) {
    return string(abi.encodePacked(a, b, c, d));
    }

    function getMagicAllFromBlason(uint _blason) public view returns (string memory) {
        string memory a = getMagicNomFromBlason(_blason);
        string memory b = getMagicDivtutFromBlason(_blason);
        string memory c = getMagicMatcoulFromBlason(_blason);
        string memory d = getMagicEvocFromBlason(_blason);
        return append(a,b,c,d);
    }



	event NewEpee(uint epeeId, string name, uint blason);
	
	event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);

	uint BlasonDigits = 4; /// @dev Représentation de l'objet magique sur 4 digits.
	uint BlasonModulus = 10 ** BlasonDigits; /// on veut que le BlasonDigits soit compris entre 0 (inclus) et 10000 (exclu)

	struct Epee { 
        string name; /// @notice une simple référence prosaïque choisie par le mal aimé pour créer une épee au départ 
        uint blason; 
        bool divin;
    }


    Epee[] public epees;  /// Tableau des épées ... 
    
    mapping (uint => address) public epeeToOwner; // @notice un userpeut posséder plusieurs épées mais une épee n'appartient qu'à un seul mal-aimé
  

   mapping (address => uint) ownerEpeeCount; // @dev Combien le mal aimé possède-t-il d'épées ?
   mapping (uint => bool) public EpeeExistence; // @dev en réserve
   

    function _inscritEpee(string _name, uint _blason, bool _divin) private {   /// @dev : inscrit l'épée
    require(!EpeeExistence[_blason], "ce pseudo existe déjà - choisissez en un autre !");
	uint id = epees.push(Epee(_name, _blason, _divin)) -1; /// @dev -1 pour retrouver l'index du tableau
	epeeToOwner[id] = msg.sender; // 
    ownerEpeeCount[msg.sender]++; // @dev le user ne peut se forger qu'un épée avec son pseudo mais peut en creuser
    // EpeeExistence[_blason] = true;  
    emit NewEpee(id, _name, _blason);	
    }

    /// @dev : on peut alors récupérer le blason en faisant dans le javascript
    /// function getBlason(id) {
    /// return <mycontract>.methods.epees(id).call()
    /// }
    /// puis faire appel aux différentes fonction pour retrouver les caractéristiques


	/// @dev dans le javascript ensuite récupérer le Blason (cf. plus haut) 
	/// string blason = 3257
	/// prendre le premier élément - le convertir en int
	/// le passer à function getMagicNom(id) {
	///  return <mycontract>.methods.magicnoms(id).call()
	///  }


  modifier onlyOwnerOf(uint _epeeId) {
    require(msg.sender == epeeToOwner[_epeeId]);
    _;
  }
   
   function _deletEpee(uint _epeeId) private {   /// @dev : détruit l'épee
    // delete epeeToOwner[_epeeId];
    epeeToOwner[_epeeId] = address(0); // adresse 0
	delete epees[_epeeId];
	// Epee storage CetteEpee = epees[_epeeId];
	// CetteEpee.divin = false; pa besoin car quand une épée est détruite elle revient à false 
    ownerEpeeCount[msg.sender] = ownerEpeeCount[msg.sender] -1 ; // le compte des épées diminue pour ce user
    }
    


function utiliser(uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    uint random = uint(blockhash(block.number-1)) % 11; // vraiment pas secure il suffit que x joue assez près du dernier bloc validé pour ne pas tomber sur 0 
    // uint256 beton = uint256(block.blockhash(block.number-1)) + uint256(adresseprivee ?)
    // uint random = beton % 11
    if (random == 0) { // Ne pas oublier de remettre à == 0
    _deletEpee(_tokenId); 
    }
  }

//  il y a des astuces :  cf. randao 
// difficile à implémenter ici


   function _forgeAleatoireBlason(string _str) private view returns (uint) { /// @dev : on va pouvoir forger des épées ...
	require(ownerEpeeCount[msg.sender] == 0, "Vous possédez encore au moins une épée"); /// @notice le mal-aimé ne peut se créer qu'un seule épée avec son pseudo (mais il peut en creuser ou  acquérir d'autres...)
        // uint aleatoire = uint(keccak256(_str));
        uint aleatoire = uint(sha256(abi.encodePacked(_str)));
        return aleatoire % BlasonModulus; 
    }	

   function creerAleatoireEpee(string _name) public {
        uint aleaBlason = _forgeAleatoireBlason(_name); /// @notice  le Blason est créé à partir du pseudo. C'est le point d'entrée de l'interface
        _inscritEpee(_name, aleaBlason, true);
        
    }
    

    function creuser() public payable {
        require(msg.value == 0.1 ether, "le montant doit être exactement de 0.1 ether"); // @dev vérifier les ethers envoyés par l'utilisateur
        uint aleatoirebis = uint(blockhash(block.number-1)) % BlasonModulus ; // @notice  même principe qu'à la création
       
        // require(!EpeeExistence[aleatoirebis], "ce blason existe déjà"); 
        
        string memory nomadhoc = "Objet magique creusé - valeur : 0.1 ether "; // il serait optimal qu'il porte le nom du  pseudo oou un nom exotique
        _inscritEpee(nomadhoc, aleatoirebis, false); // on l'inscrit
    }

    function GetEpees() public view returns (Epee[] memory) {
    uint256 nbrepees = epees.length;
    Epee[] memory listeEpees = new Epee[](nbrepees);
            for (uint256 i=0 ; i< nbrepees ; i++) {
                Epee memory e = epees[i];
                if (ownerOf(i) == msg.sender){
                listeEpees[i] = e;
                }
        }
        return listeEpees;
    }
    
  
  function ownerOf(uint256 _tokenId) public view returns (address _owner) {
    return epeeToOwner[_tokenId];
  }

  function _transfer(address _from, address _to, uint256 _tokenId) private {
      
    // on fait un test d'abord s'il ne s'agit pas d'une épee divine  
    // dans notre logique une épee divine est une épee correspondant à un pseudo..  elle ne epeut être trasnférer mais peut être utilisé
    Epee storage monEpee = epees[_tokenId];
    require(!monEpee.divin, "cette épee est divine - vous ne pouvez pas la transférer "); 
    {
    ownerEpeeCount[msg.sender] = ownerEpeeCount[msg.sender] -1;
    epeeToOwner[_tokenId] = _to;
    ownerEpeeCount[_to] = ownerEpeeCount[_to] + 1;
    emit Transfer(_from, _to, _tokenId);
    }
    
  }

  function transfer(address _to, uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    _transfer(msg.sender, _to, _tokenId);
  }



}
