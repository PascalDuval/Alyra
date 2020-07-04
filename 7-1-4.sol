pragma solidity ^0.4.19;


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




contract ApollinaireFactory {

  string[10][] public magicwords;
 
    constructor() public {
        magicwords.push(["Pâline","Noubosse", "Lul de Faltenin", "Malourène", "Sainte-Fabeau", "Chrindrono", "Annie Playden", "Lou","Marie Laurencin","Madeleine"]); 
        magicwords.push(["Vulcain", "Carabosse", "Hermes", "Avelia", "Ezheia", "Naena", "Eros", "Eros", "Eros", "Eros"]);  
        magicwords.push(["Argent", "arc-en-ciel", "bleu féminin", "fleuve vert et doré", "Gold", "métal de gloire", "Améthyste", "Saphir", "Rubis", "Larmes"]);
        magicwords.push(["gibeline", "noces", "chibriape", "riveraines", "quenouilles", "C’est l’ami aux si douces mains", "C’est un cyprès sur un tombeau", "fanfare", "dernier venu", "mal aimé"]);
    }
    
    
  function getMagicNom(uint _index) public view returns (string memory) {
        return magicwords[0][_index]; 
    }
    
  function getMagicDivtut(uint _index) public view returns (string memory) {
        return magicwords[1][_index];     }

  function getMagicMatcoul(uint _index) public view returns (string memory) {
        return magicwords[2][_index]; 
    }

  function getMagicEvoc(uint _index) public view returns (string memory) {
        return magicwords[3][_index]; 
    }



  function getMagicNomFromBlason(uint _blason) public view returns (string memory) {
        uint indexnom = _blason / 1000;
        string memory nom =  getMagicNom(indexnom);  
        return nom; 
    }

 function getMagicDivtutFromBlason(uint _blason) public view returns (string memory) {
        uint indexdivtut = (_blason - ((_blason / 1000) * 1000)) / 100;
        string memory div =  getMagicDivtut(indexdivtut);  
        return div; 
    }




 function getMagicMatcoulFromBlason(uint _blason) public view returns (string memory) {
        uint nbremilliers  = _blason / 1000;
        uint nbrecentaines  = (_blason - (nbremilliers * 1000)) / 100;
        uint nbredizaines = (_blason - (nbremilliers * 1000) - (nbrecentaines * 100)) / 10;
        uint indexmatcoul = nbredizaines; 
        string memory coul =  getMagicMatcoul(indexmatcoul);  
        return coul; 
    }

 function getMagicEvocFromBlason(uint _blason) public view returns (string memory) {
        uint nbremilliers  = _blason / 1000;
        uint nbrecentaines  = (_blason - (nbremilliers * 1000)) / 100;
        uint nbredizaines = (_blason - (nbremilliers * 1000) - (nbrecentaines * 100)) / 10;
        uint nbrunites = _blason - (nbremilliers * 1000) - (nbrecentaines * 100) - (nbredizaines * 10);
        uint indexevoc = nbrunites; 
        string memory evoc =  getMagicEvoc(indexevoc);  
        return evoc; 
    }



	event NewEpee(uint epeeId, string name, uint blason);

	uint BlasonDigits = 4; /// @dev Représentation de l'objet magique sur 4 digits.

	uint BlasonModulus = 10 ** BlasonDigits; /// on veut que le BlasonDigits soit compris entre 0 (inclus) et 10000 (exclu)



	struct Epee { 
        string name; /// @notice une simple référence prosaïque choisie par l'utilisateur (pseudo) ppour crééer 
        uint blason; /// ex : 1 en première position de BlasonDigits (ex : 1267) est "Pâline" qui est effectivement un nom ... mais poétique	
    }


    Epee[] public epees;  /// @dev : Tableau des épées ... 



   mapping (uint => address) public epeeToOwner; // deux adresses peuvent avoir le même blason néanmoins donc le jeton ne serait pas unique ?
   // mapping (address => uint) public epeeToOwner; ??

   mapping (address => uint) ownerEpeeCount; // gérer de façon unique à la création. le user ne peut s'en forger qu'une (mais peut en collecter d'autre).
	

    function _inscritEpee(string _name, uint _blason) private {   /// @dev : inscrit l'épée
	uint id = epees.push(Epee(_name, _blason)) -1; /// -1 pour retrouver l'index du tableau
	epeeToOwner[id] = msg.sender; // deux utilisateurs peuvent avoir le même blason nénamoins 
    ownerEpeeCount[msg.sender]++; // le user ne peut se forger qu'un épée néanmoins

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


   function _forgeAleatoireBlason(string _str) private view returns (uint) { /// @dev : on va pouvoir forger des épées ...
	require(ownerEpeeCount[msg.sender] == 0); /// il ne faut pas que le user possède déjà une épée à la création
        uint aleatoire = uint(keccak256(_str));
        return aleatoire % BlasonModulus; 
    }	

   function creerAleatoireEpee(string _name) public {
        uint aleaBlason = _forgeAleatoireBlason(_name); // le Blason est créé à partir du pseudo. C'est le point d'entrée
        _inscritEpee(_name, aleaBlason);
    }



}

