program kernel;

var
        i: Integer;
        scr: PChar = PChar($b8000);       

begin

        for i := 0 to 2000 do
        begin
               scr[i*2] := #65;
               scr[i*2+1] := #224;
        end;
               
               
end.

