
package Test;

// This is a comment
virtual class Human extands xxx;
    string name;
    int age;

    function new();
    endfunction

    function string getName();
    endfunction
endclass

class Boy
    extands Human; // comments

    string name;
    int age;

    function new();
    endfunction

    virtual protected static function string getName();
    endfunction

    extern virtual function int getAge();
endclass

class ABC;
endclass

endpackage