import java.util.*;

public class Disciplina {
    private String codigo;
    private String nome;
    private int creditosAula;
    private int creditosTrabalho;
    private int cargaHoraria;
    private int cargaHorariaEstagio;
    private int cargaHorariaPCC;
    private int atpa;

    public Disciplina(String codigo, String nome, int creditosAula, int creditosTrabalho, int cargaHoraria, int cargaHorariaEstagio, int cargaHorariaPCC, int atpa){
        this.codigo = codigo;
        this.nome = nome;
        this.creditosAula = creditosAula;
        this.creditosTrabalho = creditosTrabalho;
        this.cargaHoraria = cargaHoraria;
        this.cargaHorariaEstagio = cargaHorariaEstagio;
        this.cargaHorariaPCC = cargaHorariaPCC;
        this.atpa = atpa;
    }

    public String getCodigo(){return codigo;}
    public String getNome(){return nome;}
    public int getCreditosAula(){return creditosAula;}
    public int getCreditosTrabalho(){return creditosTrabalho;}
    public int getCargaHoraria(){return cargaHoraria;}
    public int getCargaHorariaEstagio(){return cargaHorariaEstagio;}
    public int getCargaHorariaPCC(){return cargaHorariaPCC;}
    public int getATPA(){return atpa;}

    @Override
    public String toString() {
        return "Disciplina {" +
               "código='" + codigo + '\'' +
               ", nome='" + nome + '\'' +
               ", créditosAula=" + creditosAula +
               ", créditosTrabalho=" + creditosTrabalho +
               ", cargaHoraria=" + cargaHoraria + "h" +
               (cargaHorariaEstagio > 0 ? ", estágio=" + cargaHorariaEstagio + "h" : "") +
               (cargaHorariaPCC > 0 ? ", PCC=" + cargaHorariaPCC + "h" : "") +
               (atpa > 0 ? ", atpas=" + atpa + "h" : "") +
               '}';
    }

    @Override
    public boolean equals(Object o){
        if(this == o) return true;
        if(o == null || getClass() != o.getClass()) return false;
        Disciplina that = (Disciplina) o;
        return Objects.equals(codigo, that.codigo);
    }

    @Override
    public int hashCode(){
        return Objects.hash(codigo);
    }
}