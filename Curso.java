import java.util.*;

public class Curso {
    private String nome;
    private String unidade;
    private String duracaoIdeal;
    private String duracaoMinima;
    private String duracaoMaxima;
    private List<Disciplina> obrigatorias;
    private List<Disciplina> optativasLivres;
    private List<Disciplina> optativasEletivas;

    public Curso(String nome, String duracaoIdeal, String duracaoMinima, String duracaoMaxima){
        this.nome = nome;
        this.duracaoIdeal = duracaoIdeal;
        this.duracaoMinima = duracaoMinima;
        this.duracaoMaxima = duracaoMaxima;
        this.obrigatorias = new ArrayList<>();
        this.optativasLivres = new ArrayList<>();
        this.optativasEletivas = new ArrayList<>();
    }

    public String getNome(){ return this.nome; }
    public String getUnidade() { return this.unidade; }
    public String getDuracaoIdeal() { return this.duracaoIdeal; }
    public String getDuracaoMinima() { return this.duracaoMinima; }
    public String getDuracaoMaxima() { return this.duracaoMaxima; }
    public List<Disciplina> getObrigatorias() { return this.obrigatorias; }
    public List<Disciplina> getOptativasLivres() { return this.optativasLivres; }
    public List<Disciplina> getOptativasEletivas() { return this.optativasEletivas; }

    @Override
    public String toString() {
        return "Curso {" + "nome = " + this.nome + "\nunidade = " + this.unidade;
    }
}
