unit libU;
{$link ./lib.o}
{$linklib gcc}
interface 
uses 
    CTypes;
procedure print; cdecl;external;
procedure clear; cdecl;external;
procedure locate; cdecl;external;
procedure print (P : Pchar);cdecl ; external;
procedure locate (x : Longint; y : Longint);cdecl ; external;
implementation

end.
