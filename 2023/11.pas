program aoc11(input, output);

type
    Cordinates = array of Integer;

    TStars = record
        xs: Cordinates;
        ys: Cordinates;
        n: Integer;
    end;

	TSpace = record
        ex: Cordinates;
        ey: Cordinates;
        m: Integer;
	end;

function parse(var f: Text): TStars;
var
    x: Integer;
    y: Integer;
    line: String;
    c: Char;
    stars: TStars;
begin
    stars.n := 0; { indices of x and y arrays}
    SetLength(stars.xs, 1024);
    SetLength(stars.ys, 1024);
    y := 0;
    while not EOF(input) do
    begin
        ReadLn(input, line);
        x := 0;
        for c in line do
        begin
            if c = '#' then
            begin
                if Length(stars.xs) <= stars.n then
                    WriteLn('Expanding..');
                    SetLength(stars.xs, Length(stars.xs) + 1024);
                if Length(stars.ys) <= stars.n then
                    SetLength(stars.ys, Length(stars.ys) + 1024);

                stars.xs[stars.n] := x;
                stars.ys[stars.n] := y;
                Inc(stars.n);
            end;
            Inc(x);
        end;
        Inc(y);
    end;
    { trim arrays }
    SetLength(stars.xs, stars.n);
    SetLength(stars.ys, stars.n);
    parse := stars;
end;

function MinIn(a: array of Integer): Integer;
var
    value, best: Integer;
begin
    best := MAXINT;
    for value in a do
        if value < best then best := value;
    MinIn := best;
end;

function MaxIn(a: array of Integer): Integer;
var
    value, best: Integer;
begin
    best := -MAXINT;
    for value in a do
        if value > best then best := value;
    MaxIn := best;
end;

operator in(i: integer; a: array of integer) result: Boolean;
var
    b: Integer;
begin
    result := false;
    for b in a do
    begin
        result := i = b;
        if result then Break;
    end;
end;

function expand_dimension(space: Cordinates): Cordinates;
var
    result: array of Integer;
    lo, hi: Integer;
    n, i: Integer;
begin
    lo := MinIn(space);
    hi := MaxIn(space);
    n := 0;
    SetLength(result, hi - lo);
    for i := lo to hi do
    begin
        if not (i in space) then
        begin
            result[n] := i;
            Inc(n);
        end;
    end;
    {trim result}
    SetLength(result, n);
    expand_dimension := result;
end;

function expand(var stars: TStars; m: Integer): TSpace;
var
    space: TSpace;
begin
    space.ex := expand_dimension(stars.xs);
    space.ey := expand_dimension(stars.ys);    
    space.m := m;
    expand := space;
end;

function manhattan1d(a: Integer; b: Integer; e: Cordinates; m: Integer): LongInt;
var
    lo, hi: Integer;
    c: Integer;
begin
    if a < b then
    begin
        lo := a;
        hi := b;
    end
    else
    begin
        lo := b;
        hi := a
    end;
    
    manhattan1d := hi - lo;
    for c in e do
    begin
        if (c >= lo) and (c < hi) then
            Inc(manhattan1d, m);
    end;
end;

function manhattan(ax, ay: Integer; bx, by: Integer; space: TSpace): LongInt;
begin
    manhattan := manhattan1d(ax, bx, space.ex, space.m) + manhattan1d(ay, by, space.ey, space.m);
end;

function distances(stars: TStars; space: TSpace): Integer;
var
    i, j: Integer;
    distance: Integer;
begin
    distances := 0;
    WriteLn('Considering ', stars.n * (stars.n - 1) div 2, ' distances...');
    for i := 0 to stars.n - 1 do
        for j := i+1 to stars.n - 1 do
        begin
            distance := manhattan(
                stars.xs[i], stars.ys[i],
                stars.xs[j], stars.ys[j],
                space
            );
            Inc(distances, distance);
        end;
end;

var
    stars: TStars;
    space: TSpace;
begin
    stars := parse(input);
    WriteLn('Loaded ', stars.n, ' stars...');
    space := expand(stars, 1);
    WriteLn('Space expanded...');
    WriteLn(distances(stars, space));
end.
