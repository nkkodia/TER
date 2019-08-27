<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0">
<xsl:output method="xml"></xsl:output>
    <xsl:template match="/">
        <xsl:for-each select="teiHeader">
        <xsl:if test="expression">
            <xsl:call-template name="structuration"></xsl:call-template>
            <xsl:text>&#xa;</xsl:text>
            ...some output if the expression is true...
        </xsl:if>
       </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="structuration">
        <xsl:variable name="text" select="unparsed-text('au_depart_de_merrien.txt', 'iso-8859-1')"></xsl:variable>
        <xsl:analyze-string select="$text" regex="([A-Z][a-z]+ *[\s|-])*[A-Z][a-z]+">
            <xsl:matching-substring>
                <xsl:text>&#xa;</xsl:text>
                <xsl:element name="NPr">
                    <xsl:value-of select="."></xsl:value-of>
                </xsl:element>
            </xsl:matching-substring>
        </xsl:analyze-string>      
    </xsl:template>
   
    <xsl:template match="NomEntite">
        <Placemark>
            <name>
                <xsl:value-of select="@name"/>
            </name>
            <xsl:text>
                        
             </xsl:text>
            <description>
                <xsl:value-of select="@idOrigine"/>
            </description>
            <xsl:text>
                        
            </xsl:text>
            <Point>
                
                <coordinates>
                    <xsl:for-each select="noeud">
                        <xsl:value-of select="@lng"/>
                        <xsl:text>,</xsl:text>
                        <xsl:value-of select="@lat"/>
                        <xsl:text>
                        
                         </xsl:text>
                    </xsl:for-each>
                    
                </coordinates>
                <xsl:text>
                        
                    </xsl:text>
                
                
                
            </Point>
        </Placemark>
    </xsl:template>
    
</xsl:stylesheet>

