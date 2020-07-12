pragma solidity ^0.4.21;
pragma experimental ABIEncoderV2;  

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/math/SafeMath.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/token/ERC721/ERC721Basic.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/token/ERC721/ERC721Receiver.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/e79dc645e4d3ad5618317f264df329f4a0f36e94/contracts/AddressUtils.sol";


/**
 * @title ERC721 Non-Fungible Token Standard basic implementation
 * @dev see https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md
 */
contract  ApollinaireToken is ERC721Basic {
    using SafeMath for uint256;
    using AddressUtils for address;
  
    string[10][] public magicwords;
  
    constructor() public {
  
  /**
   * @notice d'après un célèbre poème de G. Apollinaire : les 7 épées qu'on a étendu librement à 10
   * cf. plus bas
   * 
  */    
        magicwords.push(["Pâline ","Noubosse ", "Lul de Faltenin ", "Malourène ", "Sainte-Fabeau ", "Chrindrono ", "Annie Playden ", "Lou ","Marie Laurencin ","Madeleine "]); 
        magicwords.push(["Vulcain ", "Carabosse ", "Hermes ", "Avelia ", "Ezheia ", "Naena ", "Eros ", "Eros ", "Eros ", "Eros "]);  
        magicwords.push(["Argent ", "arc-en-ciel ", "bleu féminin ", "fleuve vert et doré ", "Gold ", "métal de gloire ", "Améthyste ", "Saphir ", "Rubis ", "Larmes "]);
        magicwords.push(["gibeline ", "noces ", "chibriape ", "riveraines ", "quenouilles ", "C’est l’ami aux si douces mains ", "C’est un cyprès sur un tombeau ", "fanfare ", "dernier venu ", "mal aimé" ]);
    }
  
 
  // Equals to `bytes4(keccak256("onERC721Received(address,uint256,bytes)"))`
  // which can be also obtained as `ERC721Receiver(0).onERC721Received.selector`
    bytes4 constant ERC721_RECEIVED = 0xf0b9e5ba;

    // event création d'une épee propre à ce contrat
	event NewEpee(uint epeeId, string name, uint blason); 
	
	uint BlasonDigits = 4; /// Représentation de l'objet magique sur 4 digits.
	uint BlasonModulus = 10 ** BlasonDigits; /// on veut que le BlasonDigits soit compris entre 0 (inclus) et 10000 (exclu)

	struct Epee { 
        string name; /// une simple référence prosaïque choisie par le user pour créer une épee au départ 
        uint blason; /// un nombre compris entre 0 et 9999 
        bool divin; /// true si forgée à partir du pseudo, false si résultat de creuser
    }

    Epee[] public epees;  /// Tableau des épées ... 

    mapping (uint256 => address) internal epeeToOwner; // internal Mapping de Epee ID au owner
    mapping (address => uint256) internal ownerEpeeCount; // Internal Mapping du owner au nombre de token(s) détenu(s)
    mapping (uint256 => address) internal tokenApprovals; // Internal Mapping du token ID à une adresse approuvée (cette adresse peut transférer le token à la plac du owner)
    mapping (address => mapping (address => bool)) internal operatorApprovals; 

   /**
   * @dev Inscrit l'épée avec cette caractéristique en lui attachant le propriétaire de départ
   * @param _name nom du pseudo (au départ) sinon un nom ad hoc
   * @param _blason un nombre sur 4 chiffres compris entre 0000 et 9999
   * @param _divin à true uniquement si elle a été créée à partir du pseudo
   */

   function _inscritEpee(string _name, uint _blason, bool _divin) private {   /// @dev : inscrit l'épée
	uint id = epees.push(Epee(_name, _blason, _divin)) -1; /// @dev -1 pour retrouver l'index du tableau
	addTokenTo(msg.sender, id); // d'une seule passe
    emit NewEpee(id, _name, _blason);	
    }
  
    /**
   * @dev Forge le Blason de l'épée au départ
   * @param _str nom du pseudo (au départ) 
   * @return le blason (entre 0 et 9999)
   */

    function _forgeAleatoireBlason(string _str) private view returns (uint) { /// @dev : on va pouvoir forger des épées ...
	require(ownerEpeeCount[msg.sender] == 0, "Vous possédez encore au moins une épée"); /// @notice le mal-aimé ne peut se créer qu'un seule épée avec son pseudo (mais il peut en creuser ou  acquérir d'autres...)
        uint aleatoire = uint(sha256(abi.encodePacked(_str)));
        return aleatoire % BlasonModulus; 
    }	

   /**
   * @dev Crée l'épée au départ
   * @param _name nom du pseudo (au départ) 
   * appelle la fonction d'inscription de l'épée
   */

   function creerAleatoireEpee(string _name) public {
        uint aleaBlason = _forgeAleatoireBlason(_name); /// @notice  le Blason est créé à partir du pseudo. C'est le point d'entrée de l'interface
        _inscritEpee(_name, aleaBlason, true);
        
    }

   /**
   * @dev Prend la balance l'addresse spécifiée
   * @param _owner addresse dont on demande la balance
   * @return uint256 represente le nombre de token détenu par l'adresse
   */
  function balanceOf(address _owner) public view returns (uint256) {
    require(_owner != address(0));
    return  ownerEpeeCount[_owner];
  }
  
    /**
   * @dev Retourne si le token spécifiée existe
   * @param _tokenId uint256 ID du token dont ondemande l'existence
   * @return si le token existe
   */
  function exists(uint256 _tokenId) public view returns (bool) {
    address owner = epeeToOwner[_tokenId];
    return owner != address(0);
  }
  
  
  /**
   * @dev Garantit que msg.sender est le owner de l'épee
   * @param _tokenId uint256 ID de l'épee pour validité qu'elle est bien la propriété du msg.sender
   */
    modifier onlyOwnerOf(uint256 _tokenId) {
    require(ownerOf(_tokenId) == msg.sender);
    _;
    }

  /**
   * @dev Vérifie que msg.sender peut transférer une épee, en étant propriétaire, approuvé, ou un opérateur
   * @param _tokenId uint256 ID du token à valider
   */
    modifier canTransfer(uint256 _tokenId) {
    require(isApprovedOrOwner(msg.sender, _tokenId));
    _;
  }

  /**
   * @dev prend le owner de l'épee spécifiée 
   * @param _tokenId uint256 ID de l'épée
   * @return retourne l'adresse du propriétaire en cours de l'épée spécifiée 
   */
  function ownerOf(uint256 _tokenId) public view returns (address) {
    address owner = epeeToOwner[_tokenId];
    require(owner != address(0));
    return owner;
  }
    

   /**
    * @dev Approuve une autre adresse pour transférer le jeton ID donné
   * @dev L'adresse zéro indique qu'il n'y a pas d'adresse approuvée.
   * @dev Il ne peut y avoir qu'une seule adresse approuvée par jeton à un moment donné.
   * @dev ne peut être appelé que par le propriétaire du token ou un opérateur approuvé.
   * @param _to l'adresse à approuver pour l'ID du jeton donné
   * @param _tokenId uint256 ID du jeton à approuver
    */

  function approve(address _to, uint256 _tokenId) public {
    address owner = ownerOf(_tokenId);
    require(_to != owner);
    require(msg.sender == owner || isApprovedForAll(owner, msg.sender));

    if (getApproved(_tokenId) != address(0) || _to != address(0)) {
      tokenApprovals[_tokenId] = _to;
      emit Approval(owner, _to, _tokenId);
    }
  }

   /**
   * @dev Obtient l'adresse approuvée pour un jeton d'identification, ou zéro si aucune adresse n'est définie
   * @param _tokenId uint256 ID du jeton pour demander l'approbation de
   * @return l'adresse actuellement approuvée pour un jeton d'identification donné
   */
   
  function getApproved(uint256 _tokenId) public view returns (address) {
    return tokenApprovals[_tokenId];
  }

   
   /**
   * @dev Définit ou annule l'approbation d'un opérateur donné
   * @dev Un opérateur est autorisé à transférer tous les jetons de l'expéditeur en son nom
   * @param _to l'adresse de l'opérateur pour définir l'approbation
   * @param _approved représente le statut de l'approbation   (true or false)
   */ 
   
  function setApprovalForAll(address _to, bool _approved) public {
    require(_to != msg.sender);
    operatorApprovals[msg.sender][_to] = _approved;
    emit ApprovalForAll(msg.sender, _to, _approved);
  }

   /**
   * @dev Indique si un opérateur est agréé par un propriétaire donné
   * @param _owner propriétaire que l'on souhaite interroger
   * @param _operator opérateur que l'on souhaite interroger
   * @return bool selon qu'un opérateur donné est approuvé par un owner donné
   */
   
   
  function isApprovedForAll(address _owner, address _operator) public view returns (bool) {
    return operatorApprovals[_owner][_operator];
  }


 /**
   * @dev Transfère la propriété d'un token ID donné à une autre adresse
   * @dev L'utilisation de cette méthode est déconseillée, utilisez "safeTransferFrom" chaque fois que possible
   * @dev Exige que le msg.sender soit propriétaire, approuvé ou opérateur
   * @param _from propriétaire actuel du jeton
   * @param _to adresse pour recevoir la propriété du jeton ID donné
   * @param _tokenId uint256 ID du jeton à transférer
  */
  
  function transferFrom(address _from, address _to, uint256 _tokenId) public canTransfer(_tokenId) {
    require(_from != address(0));
    require(_to != address(0));  
    
    // on fait un test d'abord s'il ne s'agit pas d'une épee divine  
    // dans notre logique une épee divine est une épee correspondant à un pseudo..  elle ne epeut être trasnférer mais peut être utilisé
    Epee storage monEpee = epees[_tokenId];
    require(!monEpee.divin, "cette épee est divine - vous ne pouvez pas la transférer "); 
 
    clearApproval(_from, _tokenId);
    _deletEpeeFrom(_from, _tokenId);
    addTokenTo(_to, _tokenId);
    emit Transfer(_from, _to, _tokenId);
    }


  /**
   * @dev Transfère en toute sécurité la propriété d'un jeton d'identification donné à une autre adresse
   * @dev Si l'adresse cible est un contrat, elle doit mettre en œuvre "onERC721Received",
   * qui est appelé selon un transfert sécurisé, et retourne la valeur magique
   * `bytes4(keccak256("onERC721Received(address,uint256,bytes)"))` ; sinon,
   * le transfert est annulé.
   * @dev Exige que le msg.sender soit propriétaire, approuvé ou opérateur
   * @param _from propriétaire actuel du jeton
   * @param _to l'adresse pour recevoir la propriété du jeton ID donné
   * @param _tokenId uint256 ID du jeton à transférer
  */

  
function safeTransferFrom(address _from,address _to,uint256 _tokenId) public canTransfer(_tokenId) {
  safeTransferFrom(_from, _to, _tokenId, ""); 
     }

  /**
   * @dev Transfère en toute sécurité la propriété d'un jeton d'identification donné à une autre adresse
   * @dev Si l'adresse cible est un contrat, elle doit mettre en œuvre "onERC721Received",
   * qui est appelé selon un transfert sécurisé, et retourne la valeur magique
   * `bytes4(keccak256("onERC721Received(address,uint256,bytes)"))` ; sinon,
   * le transfert est annulé.
   * @dev Exige que le msg.sender soit propriétaire, approuvé ou opérateur
   * @param _from propriétaire actuel du jeton
   * @param _to l'adresse pour recevoir la propriété du jeton ID donné
   * @param _tokenId uint256 ID du jeton à transférer
   * @param _data bytes data supplémentaire à envoyer
  */



  function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes _data) public canTransfer(_tokenId) { 
    transferFrom(_from, _to, _tokenId);
   require(checkAndCallSafeTransfer(_from, _to, _tokenId, _data));
    }


  /**
   * @dev Fonction interne pour invoquer `onERC721Received` sur une adresse cible
   * @dev L'appel n'est pas exécuté si l'adresse cible n'est pas un contrat
   * @param _from adresse de el'ancien propriétaire du jeton donné
   * @param _to adresse cible qui recevra les jetons
   * @param _tokenId uint256 ID du jeton à transférer
   * @param _data bytes données facultatives à envoyer avec l'appel
   * @return vérifiant que l'appel a correctement renvoyé la valeur magique
   */   
   
   
 function checkAndCallSafeTransfer(address _from, address _to, uint256 _tokenId, bytes _data) internal returns (bool) {
   if (!_to.isContract()) {
     return true;
   }
    bytes4 retval = ERC721Receiver(_to).onERC721Received(_from, _tokenId, _data);
    return (retval == ERC721_RECEIVED);
  }


  /**
   * @dev Indique si le spender donné peut transférer un jeton d'identification donné
   * @param _spender du dépensier à interroger
   * @param _tokenId uint256 ID du jeton à transférer
   * @return bool selon que msg.sender est approuvé pour tojen ID donné,
   * est un opérateur du propriétaire, ou est simplement le propriétaire du jeton
   */ 
   
  function isApprovedOrOwner(address _spender, uint256 _tokenId) internal view returns (bool) {
    address owner = ownerOf(_tokenId);
    return _spender == owner || getApproved(_tokenId) == _spender || isApprovedForAll(owner, _spender);
  }

    /**
   * @dev Fonction interne permettant de valider l'approbation actuelle d'un jeton d'identification donné
   * @dev Reverts si l'adresse donnée n'est pas effectivement le propriétaire du jeton
   * @param _owner propriétaire du jeton
   * @param _tokenId uint256 ID du jeton à transférer
   */ 
   
  function clearApproval(address _owner, uint256 _tokenId) internal {
    require(ownerOf(_tokenId) == _owner);
    if (tokenApprovals[_tokenId] != address(0)) {
      tokenApprovals[_tokenId] = address(0);
      emit Approval(_owner, address(0), _tokenId);
    }
  }


   /**
   * @dev Fonction interne permettant d'ajouter un token ID à la liste d'une adresse donnée
   * @param _to adresse représentant le nouveau propriétaire du jeton d'identification donné
   * @param _tokenId uint256 ID du jeton à ajouter à la liste des jetons de l'adresse donnée
   */ 
   
  function addTokenTo(address _to, uint256 _tokenId) internal {
    require(epeeToOwner[_tokenId] == address(0)); // il doit être libre.. 
    epeeToOwner[_tokenId] = _to;
    ownerEpeeCount[_to] = ownerEpeeCount[_to].add(1);
   }
  
 

  /**
   * @dev fonction Internal pour enlever un token ID de la liste d'une adresse donnée
   * @param _tokenId uint256 ID du token ID qui doit être enlevé 
   * @param _from adresse représentant le détenteur précédent du token ID en question
 */
 
   function _deletEpeeFrom(address _from, uint _tokenId) internal { 
    require(ownerOf(_tokenId) == _from);   
    clearApproval(_from, _tokenId); // ajout
    ownerEpeeCount[msg.sender] = ownerEpeeCount[msg.sender].sub(1);
    epeeToOwner[_tokenId] = address(0); // adresse 0
    }

 /**
   * @dev fonction pour utiliser un token ID 
   * @param _tokenId uint256 ID du token ID 
   * @notice il y a un risque.. 
 */

    function _utiliser(uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    uint random = uint(blockhash(block.number-1)) % 11; // vraiment pas secure il suffit que x joue assez près du dernier bloc validé pour ne pas tomber sur 0 
    if (random == 0) { 
    _deletEpeeFrom(msg.sender,_tokenId); 
    }
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




  
  /**
   * @notice fonctions diverses permettant de renvoyer les données du token
   * un token comprend un nom, un blason (un nombre entre 0 et 9999) et une information (divin ou pas)
   * le nom est le pseudo à partir duquel a été créée la première épée -  il est divin et ne peut-être transféré
   * Le Blason 8021 se décompose ainsi :
   * 8 : index 8 du tableau des noms magiques (c'est le nom de l'épée et non le nom du pseudo)
   * 0 : index 0 du tableau des divinités tutélaires
   * 2 : index 2 des matières ou couleurs 
   * 1 : index 1 
   * 
 */
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

/// @notice Les sept épées  du Recueil "Alcools"
/// @auteur Guillaume Apollinaire
/// @auteur Pascal Duval

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
///    Adieu voilà votre chemin
///    Les coqs s’épuisaient en fanfares

///    Et la septième s’exténue
///    Une femme une rose morte
///    Merci que le dernier venu
///    Sur mon amour ferme la porte
///    Je ne vous ai jamais connue  

  
    
}


