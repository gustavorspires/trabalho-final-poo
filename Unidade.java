import java.util.*;

public class Unidade {
    private String nome;
    private List<Curso> cursos;

    public Unidade(String nome){
        this.nome = nome;
        this.cursos = new ArrayList<>();
    }

    public String getNome(){ return this.nome; }
    public List<Curso> getCursos() { return this.cursos; }

    public void addCurso(Curso curso){
        this.cursos.add(curso);
    }

    @Override
    public String toString(){
        return "Unidade: " + this.nome + "\nCursos: " + this.cursos.toString();
    }
}


